const hoy = new Date()
const dd = hoy.getDate();
let mm = hoy.getMonth()+1;
let yyyy = hoy.getFullYear();
const months = {
    1:'Enero',
    2:'Febrero',
    3:'Marzo',
    4:'abril',
    5:'Mayo',
    6:'Junio',
    7:'Julio',
    8:'Agosto',
    9:'Septiembre',
    10:'Octubre',
    11:'Noviembre',
    12:'Diciembre',
}
let gameList = []

function loadCalendar(){
    const $actualMonth = document.getElementById('month_label')
    $actualMonth.innerHTML = months[mm]
    $actualMonth.dataset.number = mm
    const $actualYear = document.getElementById('year_label')
    $actualYear.innerHTML = yyyy
    $actualYear.dataset.number = yyyy
    
    fillCalendar()
    removeLastDay(mm)
    addEvents()
    
}

function fillCalendar(){
    fetch('/profile/games')
        .then((response)=>{
            return jsonify_response = response.json()

        })
        .then((games)=>{
            
            gameList = games
            selectCalendar()
        })
        

}

function selectCalendar(){
    const $dataMonth = parseInt(document.getElementById('month_label').dataset.number)
    const $dataYear = parseInt(document.getElementById('year_label').dataset.number)
    for (const game of gameList) {
        const gameDate = game.id.split('-')
        const gameMonth = parseInt(gameDate[1])
        const gameYear = parseInt(gameDate[0])
        if($dataMonth === gameMonth && $dataYear === gameYear){
            addGame(gameDate, game)
        }
    }
}

function addEvents(){
    const $leftArrow = document.getElementById('calendar__left')
    const $rightArrow = document.getElementById('calendar__right')
    for(let i=0; i < 31; i++){
        $component = document.getElementById(`day-${i+1}`)
        $component.addEventListener('click', viewDay.bind(this))
    }
    $leftArrow.addEventListener('click', lastMonth)
    $rightArrow.addEventListener('click', nextMonth)
}

function removeEvents(){

}

function lastMonth(){
    const $actualMonth = document.getElementById('month_label')
    let monthToChange = $actualMonth.dataset.number
    if(monthToChange == 1){
        monthToChange = 13
        yyyy--
        const $actualYear = document.getElementById('year_label')
        $actualYear.innerHTML = yyyy
        $actualYear.dataset.number = yyyy
    }
    newDataset = monthToChange - 1
    mm = newDataset
    $actualMonth.dataset.number = newDataset
    $actualMonth.innerHTML = months[newDataset]
    removeGames()
    removeLastDay(newDataset)
    selectCalendar()
}

function nextMonth(){
    const $actualMonth = document.getElementById('month_label')
    let monthToChange = parseInt($actualMonth.dataset.number)
    if(monthToChange == 12){
        monthToChange = 0
        yyyy++
        const $actualYear = document.getElementById('year_label')
        $actualYear.innerHTML = yyyy
        $actualYear.dataset.number = yyyy
    }
    newDataset = monthToChange + 1
    mm = newDataset
    $actualMonth.dataset.number = newDataset
    $actualMonth.innerHTML = months[newDataset]
    removeGames()
    removeLastDay(newDataset)
    selectCalendar()
}

function removeLastDay(month){
    const largeMonths = [1, 3, 5, 7, 8, 10, 12];
    const shortMonths = [2, 4, 6, 9, 11];
    const $leapDay = document.getElementById('day-30')
    const $noLeapDay = document.getElementById('day-29')
    const leapYear = (yyyy%4 === 0)? true : false
    for (let i = 0; i < shortMonths.length; i++) {

        if(month == shortMonths[i]){
            removeDay(31)

            if(!leapYear && month === 2){ removeDay(29) }
    
            if(month === 2){ removeDay(30) }
            
            break

        }else if(month == largeMonths[i]){
            addDay(31)

            if(!$leapDay.classList.contains('day-30')){ addDay(30) }

            if(!$noLeapDay.classList.contains('day-29')){ addDay(29) }

            break

        }
    }
}

function removeDay(day){
    const $component = document.getElementById(`day-${day}`)
    $component.innerHTML = ''
    $component.classList.remove(`day-${day}`)

}
function addDay(day){
    const $component = document.getElementById(`day-${day}`)
    $component.innerHTML = `${day}`
    $component.classList.add(`day-${day}`)
}

function addGame(gameDate, game){
    const gameTime = gameDate[2].split('T')[1].split(':')
    const gameDay = parseInt(gameDate[2].split('T')[0])
    const $calendarDay = document.getElementById(`day-${gameDay}`)
    const badge = document.createElement('span')
    const text = document.createTextNode(`${gameTime[0]}:${gameTime[1]}`)
    badge.appendChild(text)
    badge.classList.add('badge')
    if(game.training){
        badge.classList.add('badge-success')
    }else{
        badge.classList.add('badge-info')
    }
    addClickEvent(badge, calificar)
    $calendarDay.appendChild(badge)

    
}

function removeGames(){
    // debugger
    let games = document.getElementsByClassName('badge')
    for (let i=0; games.length > 0; i){
        let parent = games[i].parentNode
        parent.removeChild(games[i])
    }
}

function addClickEvent(Element, func){
    Element.addEventListener('click', func)
}

function viewDay(ev){
    ev.preventDefault()

    const day = ev.target.dataset.number
    const $calendarBody = document.getElementById('calendar__body')
    const overlay = document.createElement('div')
    const divContent = document.createElement('div')
    const closeBtn = document.createElement('div')
    const x = document.createTextNode('x')
    
    addClickEvent(closeBtn, closeViewDay)


    closeBtn.classList.add('overlay__close-btn')
    overlay.classList.add('calendar__overlay')
    divContent.classList.add('overlay__content')
    overlay.setAttribute('id', 'calendar__overlay')


    closeBtn.appendChild(x)
    overlay.appendChild(closeBtn)
    overlay.appendChild(divContent)
    $calendarBody.appendChild(overlay)
    fillOverlayContent(divContent, day)
}

function closeViewDay(){
    const overlay = document.getElementById('calendar__overlay')
    const parent = overlay.parentNode
    parent.removeChild(overlay)
}

function fillOverlayContent(div, day){
    // debugger
    const month = document.getElementById('month_label').dataset.number
    const year = document.getElementById('year_label').dataset.number
    const date = document.createElement('p')
    const dateTxt = document.createTextNode(`${day} de ${months[month]} del ${year}`)
    const form = document.createElement('form')
    const csrfInput = window.csrf_token
    const locationInput = document.createElement('input')
    const timeInput = document.createElement('input')
    const trainingRadio = document.createElement('input')
    const gameRadio = document.createElement('input')
    const trainigLabel = document.createElement('label')
    const gameLabel = document.createElement('label')
    const training = document.createTextNode('Entrenamiento')
    const game = document.createTextNode('Partido')
    const submitBtn = document.createElement('input')
    const dateInput = document.createElement('input')

    date.appendChild(dateTxt)
    form.setAttribute('action', '/profile/add_game')
    form.setAttribute('method', 'POST')
    // csrfInput.setAttribute('id', 'csrf_token')
    // csrfInput.setAttribute('name', 'csrf_token')
    // csrfInput.setAttribute('type', 'hidden')
    // csrfInput.setAttribute('value', window.csrf_token)
    locationInput.setAttribute('type', 'text')
    locationInput.setAttribute('name', 'location')
    locationInput.setAttribute('placeholder', 'Lugar')
    locationInput.setAttribute('required','')
    timeInput.setAttribute('type', 'time')
    timeInput.setAttribute('name', 'time')
    timeInput.setAttribute('required','')
    gameRadio.setAttribute('type', 'radio')
    gameRadio.setAttribute('name', 'training')
    gameRadio.setAttribute('id', 'game')
    gameRadio.setAttribute('value', 'false')
    gameRadio.setAttribute('required','')
    trainingRadio.setAttribute('type', 'radio')
    trainingRadio.setAttribute('name', 'training')
    trainingRadio.setAttribute('id', 'training')
    trainingRadio.setAttribute('value', 'true')
    trainigLabel.setAttribute('for', 'training')
    gameLabel.setAttribute('for', 'game')
    submitBtn.setAttribute('type', 'submit')
    dateInput.setAttribute('type', 'hidden')
    dateInput.setAttribute('value', `${year}-${month}-${day}`)
    dateInput.setAttribute('name', 'date')

    div.appendChild(date)
    form.append(csrfInput)
    form.appendChild(locationInput)
    form.appendChild(timeInput)
    trainigLabel.appendChild(training)
    gameLabel.appendChild(game)
    form.appendChild(trainigLabel)
    form.appendChild(trainingRadio)
    form.appendChild(gameLabel)
    form.appendChild(gameRadio)
    form.appendChild(submitBtn)
    form.appendChild(dateInput)
    div.appendChild(form)

}

function calificar(ev){
    ev.stopPropagation();
    year = document.getElementById('year_label').dataset.number
    month = document.getElementById('month_label').dataset.number
    day = ev.target.parentNode.dataset.number
    hour = ev.target.innerHTML
    window.location.replace(`/crud/assess?year=${year}&month=${month}&day=${day}&hour=${hour}`)
}

/* <p id="month_label"></p>
<p id="year_label"></p> */