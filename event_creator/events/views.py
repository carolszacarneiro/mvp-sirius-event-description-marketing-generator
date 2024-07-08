import openai
from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event

# Configure sua chave de API da OpenAI aqui
openai.api_key = 'sua-chave-de-api'

def generate_event_description(name, date, location, price, capacity):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Crie uma descrição para um evento chamado {name}, que ocorrerá em {date} no local {location}. O preço do ingresso é {price} e a capacidade é de {capacity} pessoas.",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_event_banner(name):
    response = openai.Image.create(
        prompt=f"Crie um banner para um evento chamado {name}",
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.description = generate_event_description(
                event.name, event.date, event.location, event.price, event.capacity)
            event.banner_url = generate_event_banner(event.name)
            event.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})
