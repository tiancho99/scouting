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

function loadCalendar(games){
    
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
    fetch('http://127.0.0.1:5000/profile/games')
        .then((response)=>{
            return jsonify_response = response.json()

        })
        .then((games)=>{
            console.log(games)
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
        badge.classList.add('badge-secondary')
    }else{
        badge.classList.add('badge-primary')
    }
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


function viewDay(ev){
    ev.preventDefault()
    console.log(ev.target.dataset.number)
}