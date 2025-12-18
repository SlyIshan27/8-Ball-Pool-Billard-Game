let track = false;
let line = null;
let cueBallCenterX, cueBallCenterY;
let cueBallClicked = false;
let mouseX = null;
let mouseY = null;
let removeLineEnabled = true
let lastSVG = null;
let turn = null;
let player1Name = null;
let player2Name = null;
let animationFinished = true;


function trackon() {
    console.log("Hit")
    if(!track){
        track = true;
        cueBallClicked = true;
        const cueBall = document.querySelector('circle[fill="WHITE"]');
        // const cueBallRect = cueBall.getBoundingClientRect();
        // cueBallCenterX = cueBallRect.left + cueBallRect.width / 2;
        // cueBallCenterY = cueBallRect.top + cueBallRect.height / 2;

        cueBallCenterX = parseInt(cueBall.getAttribute('cx'));
        cueBallCenterY = parseInt(cueBall.getAttribute('cy'));
        console.log(cueBallCenterX);
        
    }
}

function removeLine(event){

    if (removeLineEnabled && track && animationFinished) {
        if(event.target.getAttribute('fill') !== 'WHITE'){
            removeLineEnabled = false
            animationFinished = false
        
            line.remove();
            cueBallClicked = false; // Reset cue ball clicked
            // track = false;
            var cueBall = document.querySelector('circle[fill="WHITE"]');
            var cueBallX = parseInt(cueBall.getAttribute('cx'));
            var cueBallY = parseInt(cueBall.getAttribute('cy'));
            console.log("Cue Ball X: ", cueBallX);
            console.log("Cue Ball Y: ", cueBallY);
            console.log("X coordinate: ", mouseX);
            console.log("Y coordinate: ", mouseY);

            // var deltaX = mouseX - cueBallX;
            // var deltaY = mouseY - cueBallY;
            // // var scaleFactor = 0.8;

            // var initialVelX = deltaX
            // var initialVelY = deltaY 
            var distance = Math.sqrt(Math.pow(mouseX - cueBallX, 2) +
            Math.pow(mouseY - cueBallY, 2));

            var XVector = (mouseX - cueBallX) / distance;
            var YVector = (mouseY - cueBallY) / distance;

            var v = Math.min(5.8 * distance, 10000);
            var initialVelX = XVector * v;
            var initialVelY = YVector * v;
            console.log("Intial Velocity X: ", initialVelX);
            console.log("Intial Velocity Y: ", initialVelY);

            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/initial-velocity", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                        // console.log("Shot Processed Succesfully");
                        try{
                            // var data = JSON.stringify(xhr.responseText)
                            var svgString = xhr.responseText;
                            var svgs = svgString.split("---");
                            // console.log("Success FINALLLY: ", svgs);
                            animateSVG(svgs);
                        } catch (e){
                            console.error("Error:", e);
                        }
                }
            };
            var data = JSON.stringify({ initialVelX: initialVelX, initialVelY: initialVelY, turn: turn, cueBallX: cueBallX, cueBallY: cueBallY });
            xhr.send(data);

            // if(turn == 1){
            //     turn = 2;
            // }else{
            //     turn = 1;
            // }
            // xhr.send();
            track = false
            removeLineEnabled = true
        }
        
    } /*else {
        track = true; // Set track to true if line doesn't exist
        cueBallClicked = true; // Set cue ball clicked to true
    }*/

}


function getSVGMouse(event, SVGObject) {
    const point = document.createElementNS('http://www.w3.org/2000/svg', 'svg').createSVGPoint();
    point.x = event.clientX;
    point.y = event.clientY;
    return point.matrixTransform(SVGObject.getScreenCTM().inverse());
}

function trackit(event) {
    if (track && cueBallClicked) {
        $('#valx').remove();
        $('#valy').remove();
        $('<div id="valx">' + event.pageX + '</div>').appendTo("#x");
        $('<div id="valy">' + event.pageY + '</div>').appendTo("#y");

        if (line) {
            line.remove();
        }

        const svg = document.getElementById('poolTable');
        
        const svgMouse = getSVGMouse(event, svg);
        mouseX = svgMouse.x;
        mouseY = svgMouse.y;
        // const mouseX = event.clientX;
        // const mouseY = event.clientY;


        // Calculate line angle
        // const dx = mouseX - cueBallCenterX;
        // const dy = mouseY - cueBallCenterY;
        // let angle = Math.atan2(dy, dx);

        // if (angle < 0) {
        //     angle += 2 * Math.PI;
        // }


        // // Adjust line length to make it reach far beyond the current mouse position
        // const length = Math.sqrt(dx * dx + dy * dy) * 0.2; // Increase the length factor if needed

        // // Calculate endpoint coordinates
        // const endX = cueBallCenterX + length * Math.cos(angle);
        // const endY = cueBallCenterY + length * Math.sin(angle);


        // Create and append the line element
        line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", cueBallCenterX);
        line.setAttribute("y1", cueBallCenterY);
        line.setAttribute("x2", mouseX);
        line.setAttribute("y2", mouseY);
        line.setAttribute("stroke", "black");
        line.setAttribute("stroke-width", "5");
        svg.appendChild(line);
    }
}

function animateSVG(svgData) {
    // clearInterval(intervalId); // Clear any existing animation interval
    let i = 0;
    intervalId = setInterval(() => {
        // console.log("Current index:", i);
        // console.log("Total SVGs:", svgData.length);
        if (i < svgData.length) {
            renderSVG(svgData[i]);
            i++;
        } else {
            clearInterval(intervalId); // Stop the interval when all SVGs have been rendered
            console.log("Animation completed");
            animationFinished = true;
            processShot(lastSVG);
        }
    }, 10); // Adjust the delay (in milliseconds) between each SVG rendering as needed
    
    lastSVG = svgData[svgData.length - 1]
    if(turn == 1){
        console.log("Hit Turn Change 1");
        document.getElementById("turn").innerHTML = 'Player Turn: ' + player2Name;
        console.log(player2Name);
    }else{
        console.log("Hit Turn Change 2");
        document.getElementById("turn").innerHTML = 'Player Turn: ' + player1Name;
        console.log(player1Name);
    }



}

function processShot(lastSVG){
    result = ""
    if(lastSVG.includes("cueBall")){
        console.log("Contains Cue Ball")
        result = lastSVG
        attachCueBallListener();
    }else{
        // modifiedSVG = lastSVG.replace("</svg>", "");
        // result = modifiedSVG.concat('<circle id="cueBall" cx="677" cy="2025" r="28" fill="WHITE"/> \n </svg>');
        // $('#poolTable').replaceWith(result);
        const cueBall = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "circle"
        );
        const svg = document.getElementById('poolTable');
        cueBall.setAttribute("id", "cueBall");
        cueBall.setAttribute("cx", 677);
        cueBall.setAttribute("cy", 2025);
        cueBall.setAttribute("r", 28);
        cueBall.setAttribute("fill", "WHITE");

        svg.appendChild(cueBall);

        attachCueBallListener();
        console.log("Replaced Cue Ball");
        result = svg
    }
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/process-shot", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
                // console.log("Shot Processed Succesfully");
                try{
                    // var data = JSON.stringify(xhr.responseText)
                    var highOrLow = xhr.responseText;
                    console.log(highOrLow)

                    if(highOrLow === 'LOW'){
                        if(turn == 1){
                            document.getElementById("player1").innerHTML = 'Player Turn: ' + player1Name + '\n LOW';
                            document.getElementById("player2").innerHTML = 'Player Turn: ' + player2Name + '\n HIGH';
                        }else{
                            document.getElementById("player2").innerHTML = 'Player Turn: ' + player2Name + '\n LOW';
                            document.getElementById("player11").innerHTML = 'Player Turn: ' + player1Name + '\n HIGH';
                        }
                    }else if(highOrLow === 'HIGH'){
                        if(turn == 1){
                            document.getElementById("player1").innerHTML = 'Player Turn: ' + player1Name + '\n HIGH';
                            document.getElementById("player2").innerHTML = 'Player Turn: ' + player2Name + '\n LOW';
                        }else{
                            document.getElementById("player2").innerHTML = 'Player Turn: ' + player2Name + '\n HIGH';
                            document.getElementById("player1").innerHTML = 'Player Turn: ' + player1Name + '\n LOW';
                        }
                    }
                    
                } catch (e){
                    console.error("Error:", e);
                }
        }
    };
    var data = JSON.stringify({ result: result });
    xhr.send(data);

    if(turn == 1){
        turn = 2
        console.log("Hit Turn Change 1");
        document.getElementById("turn").innerHTML = 'Player Turn: ' + player2Name;
        console.log(player2Name);
    }else{
        turn = 1
        console.log("Hit Turn Change 2");
        document.getElementById("turn").innerHTML = 'Player Turn: ' + player1Name;
        console.log(player1Name);
    }
}

function renderSVG(svgString){
    // $('#poolTable').empty();
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgString, "image/svg+xml");
    const newSVG = doc.documentElement;

    const oldSVG = document.getElementById("poolTable");
    if (!oldSVG) return;

    newSVG.setAttribute("id", "poolTable");
    // Replace ONLY the children, not the SVG itself
    oldSVG.replaceWith(newSVG);
    // // Append the new SVG content to the element
    // $('#poolTable').append(svgString);
    // $('#poolTable').replaceWith(svgString);
//     let cleanedSvgString = svgString.replace(/<\?xml.*?\?>\n/, '').replace(/<!DOCTYPE.*?>\n/, '');

// // Remove the opening and closing <svg> tags
//     cleanedSvgString = cleanedSvgString.replace(/<svg.*?>/, '').replace(/<\/svg>/, '');
    // document.getElementById('poolTable').innerHTML = svgString;

    // console.log(cleanedSvgString);

}

// $(document).ready(function() {
//     fetchSVGData();
//     console.log("Hit")
// });

function randomIntFromInterval(min, max) { // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min)
  }

function attachCueBallListener() {
    const cueBall = document.getElementById('cueBall');
    if (cueBall) {
        cueBall.addEventListener('click', trackon);
    }
}


document.addEventListener('click', removeLine);

// document.getElementById('poolTable').addEventListener('click', function(event) {
//     if (event.target && event.target.id === 'cueBall') {
//         console.log("Cue Ball clicked");
//         trackon();
//     }
// });

document.addEventListener('DOMContentLoaded', function() {
    var cueBall = document.querySelector('circle[fill="WHITE"]');
    cueBall.addEventListener('click', function() {
        console.log("Hit PUII");
        trackon();
    })


    var svg = document.getElementById('poolTable');

    // svg.addEventListener('click', function() {
    //     console.log("HIT SVG NOO");
    // })

    var svg = document.getElementById('cueBall');

    svg.addEventListener('click', function() {
        console.log("HIT Cue Ball");
    })

    const urlParams = new URLSearchParams(window.location.search);
    player1Name = urlParams.get('player1Name');
    player2Name = urlParams.get('player2Name');

    turn = randomIntFromInterval(1,2);
    console.log('Player 1:', player1Name);
    console.log('Player 2:', player2Name);

    document.querySelector('.playerOne').innerText = 'Player 1: ' + player1Name + '\n(LOW/HIGH)';;
    document.querySelector('.playerTwo').innerText = 'Player 2: ' + player2Name + '\n(LOW/HIGH)';;
    if(turn == 1){
        document.querySelector('.turn').innerText = 'Player Turn: ' + player1Name;
    }else{
        document.querySelector('.turn').innerText = 'Player Turn: ' + player2Name;
    }



});
