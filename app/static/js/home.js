const hoy = new Date()
const dd = hoy.getDate();
const mm = hoy.getMonth()+1;
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
let games = ''
function loadCalendar(games){
    fetch('http://127.0.0.1:5000/profile/games')
        .then((response)=>{
            return jsonify_response = response.json()

        })
        .then((games)=>{
            window.games = games
            fillCalendar(games)
        })
        

}

function fillCalendar(games){

    const $actualMonth = document.getElementById('month_label')
    $actualMonth.innerHTML = months[mm]
    $actualMonth.dataset.number = mm
    const $actualYear = document.getElementById('year_label')
    $actualYear.innerHTML = yyyy

    
    removeLastDay(mm)
    addEvents()

}

function addEvents(){
    const $leftArrow = document.getElementById('calendar__left')
    const $rightArrow = document.getElementById('calendar__right')
    $leftArrow.addEventListener('click', lastMonth)
    $rightArrow.addEventListener('click', nextMonth)
}

function lastMonth(){
    const $actualMonth = document.getElementById('month_label')
    let monthToChange = $actualMonth.dataset.number
    if(monthToChange == 1){
        monthToChange = 13
        yyyy--
        const $actualYear = document.getElementById('year_label')
        $actualYear.innerHTML = yyyy
    }
    newDataset = monthToChange - 1
    $actualMonth.dataset.number = newDataset
    $actualMonth.innerHTML = months[newDataset]
    removeLastDay(newDataset)
}

function nextMonth(){
    const $actualMonth = document.getElementById('month_label')
    let monthToChange = parseInt($actualMonth.dataset.number)
    if(monthToChange == 12){
        monthToChange = 0
        yyyy++
        const $actualYear = document.getElementById('year_label')
        $actualYear.innerHTML = yyyy
    }
    newDataset = monthToChange + 1
    $actualMonth.dataset.number = newDataset
    $actualMonth.innerHTML = months[newDataset]
    removeLastDay(newDataset)
}

function removeLastDay(month){
    const largeMonths = [1, 3, 5, 7, 8, 10, 12];
    const shortMonths = [2, 4, 6, 9, 11];
    const $lastDay = document.getElementById('day-31')
    const $leapDay = document.getElementById('day-30')
    const $noLeapDay = document.getElementById('day-29')
    const leapYear = (yyyy%4 === 0)? true : false
    for (let i = 0; i < shortMonths.length; i++) {

        if(month == shortMonths[i]){
            $lastDay.innerHTML = ''
            $lastDay.classList.remove('day-31')
            if(!leapYear && month === 2){
                $leapDay.innerHTML = ''
                $leapDay.classList.remove('day-30')
                $noLeapDay.innerHTML = ''
                $noLeapDay.classList.remove('day-29')
            }else if(leapYear && month === 2){
                $leapDay.innerHTML = ''
                $leapDay.classList.remove('day-30')
            }
            break
        }else if(month == largeMonths[i]){
            $lastDay.innerHTML = '31'
            $lastDay.classList.add('day-31')
            if(!$leapDay.classList.contains('day-30')){
                $leapDay.innerHTML = '30'
                $leapDay.classList.add('day-30')
            }
            if(!$noLeapDay.classList.contains('day-29')){
                $noLeapDay.innerHTML = '29'
                $noLeapDay.classList.add('day-29')
            }
            break
        }

    }
}

function removeDay(day){
    const component = document.getElementById(`day-${day}`)
    component.innerHTML = ''
    component.classList.remove(`day-${day}`)

}
function addDay(day){
    const component = document.getElementById(`day-${day}`)
    component.innerHTML = `${day}`
    component.classList.add(`day-${day}`)
}
