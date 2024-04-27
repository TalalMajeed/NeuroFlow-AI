let canvas = document.querySelector("#main-canvas");
let ctx = canvas.getContext("2d");
let text = document.querySelector("#text");

let canvasWidth = canvas.width;
let canvasHeight = canvas.height;
let tileSize = 40;

console.log(canvasWidth, canvasHeight);

window.addEventListener("resize", () => {
    canvasWidth = canvas.width;
    canvasHeight = canvas.height;
    drawGrid();
});

const standardSize = 40;

let offsetX = 0;
let offsetY = 0;

boxes = [
    ["b1", 40, 40, 300, 60, "#2094AB", "Hello World", [0, 0, 0, 0], false],
    ["b2", 500, 150, 200, 60, "#2094AB", "This is Box 2", [0, 0, 0, 0], false],
    ["b3", 200, 400, 200, 150, "#2094AB", "Test Box", [0, 0, 0, 0], false],
];

function getCanvasCoordinates(canvas) {
    const rect = document.querySelector("#main-canvas").getBoundingClientRect();
    return {
        x: rect.left + window.scrollX,
        y: rect.top + window.scrollY,
    };
}

function roundRect(
    ctx,
    x,
    y,
    width,
    height,
    radius = 5,
    fill = false,
    stroke = true,
    color = "#000",
    text
) {
    radius = (radius / standardSize) * tileSize;
    if (typeof radius === "number") {
        radius = { tl: radius, tr: radius, br: radius, bl: radius };
    } else {
        radius = { ...{ tl: 0, tr: 0, br: 0, bl: 0 }, ...radius };
    }
    ctx.beginPath();
    ctx.moveTo(x + radius.tl, y);
    ctx.lineTo(x + width - radius.tr, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr);
    ctx.lineTo(x + width, y + height - radius.br);
    ctx.quadraticCurveTo(
        x + width,
        y + height,
        x + width - radius.br,
        y + height
    );
    ctx.lineTo(x + radius.bl, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl);
    ctx.lineTo(x, y + radius.tl);
    ctx.quadraticCurveTo(x, y, x + radius.tl, y);
    ctx.closePath();
    if (fill) {
        ctx.fillStyle = color;
        ctx.fill();
    }
    if (stroke) {
        ctx.strokeStyle = color;
        ctx.stroke();
    }
    ctx.fillStyle = "#fff";
    ctx.font = "normal " + (18 / standardSize) * tileSize + "px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(text, x + width / 2, y + height / 2);
}

function drawGrid() {
    ctx.strokeStyle = "#ccc";
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    ctx.beginPath();

    let i = 0;
    for (
        i = offsetX % tileSize;
        i < canvasWidth + tileSize * 2;
        i += tileSize
    ) {
        ctx.moveTo(i + 0.5, 0 + 0.5);
        ctx.lineTo(i + 0.5, canvasHeight + 0.5);
        ctx.stroke();
    }

    for (
        i = offsetY % tileSize;
        i < canvasHeight + tileSize * 2;
        i += tileSize
    ) {
        ctx.beginPath();
        ctx.moveTo(0 + 0.5, i + 0.5);
        ctx.lineTo(canvasWidth + 0.5, i + 0.5);
        ctx.stroke();
    }

    for (let i = 0; i < boxes.length; i++) {
        ctx.fillStyle = boxes[i][5];

        roundRect(
            ctx,
            (boxes[i][1] / standardSize) * tileSize + offsetX,
            (boxes[i][2] / standardSize) * tileSize + offsetY,
            (boxes[i][3] / standardSize) * tileSize,
            (boxes[i][4] / standardSize) * tileSize,
            10,
            true,
            false,
            boxes[i][5],
            boxes[i][6]
        );

        if (boxes[i][7] == true) {
            ctx.strokeStyle = "#0362fc";

            ctx.strokeRect(
                (boxes[i][1] / standardSize) * tileSize + offsetX - 4,
                (boxes[i][2] / standardSize) * tileSize + offsetY - 4,
                (boxes[i][3] / standardSize) * tileSize + 8,
                (boxes[i][4] / standardSize) * tileSize + 8
            );

            ctx.beginPath();
            ctx.arc(
                (boxes[i][1] / standardSize) * tileSize + offsetX - 4,
                (boxes[i][2] / standardSize) * tileSize + offsetY - 4,
                5,
                0,
                2 * Math.PI
            );
            ctx.strokeStyle = "#0362fc";
            ctx.fill();
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(
                (boxes[i][1] / standardSize) * tileSize +
                    offsetX +
                    (boxes[i][3] / standardSize) * tileSize +
                    4,
                (boxes[i][2] / standardSize) * tileSize + offsetY - 4,
                5,
                0,
                2 * Math.PI
            );
            ctx.strokeStyle = "#0362fc";
            ctx.fill();
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(
                (boxes[i][1] / standardSize) * tileSize + offsetX - 4,
                (boxes[i][2] / standardSize) * tileSize +
                    offsetY +
                    (boxes[i][4] / standardSize) * tileSize +
                    4,
                5,
                0,
                2 * Math.PI
            );
            ctx.strokeStyle = "#0362fc";

            ctx.fill();
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(
                (boxes[i][1] / standardSize) * tileSize +
                    offsetX +
                    (boxes[i][3] / standardSize) * tileSize +
                    4,
                (boxes[i][2] / standardSize) * tileSize +
                    offsetY +
                    (boxes[i][4] / standardSize) * tileSize +
                    4,
                5,
                0,
                2 * Math.PI
            );
            ctx.strokeStyle = "#0362fc";
            ctx.fill();
            ctx.stroke();
        }
    }
}
drawGrid();

let isDragging = false;
let startX = 0;
let startY = 0;
let bstartX = 0;
let bstartY = 0;
let mousePressed = false;
let currentButton = -1;
let activeIndex = -1;
let editIndex = -1;
let isResizing = false;
let resizeDirection = "";
let initialWidth = 0;
let initialHeight = 0;

function zoom(e) {
    e.preventDefault();
    const mouseX = e.clientX - canvas.getBoundingClientRect().left;
    const mouseY = e.clientY - canvas.getBoundingClientRect().top;

    const prevTileSize = tileSize;

    if (e.deltaY < 0) {
        if (tileSize < 60) {
            tileSize += 2;
        }
    } else {
        if (tileSize > 20) {
            tileSize -= 2;
        }
    }

    const scaleFactor = tileSize / prevTileSize;
    offsetX = mouseX - (mouseX - offsetX) * scaleFactor;
    offsetY = mouseY - (mouseY - offsetY) * scaleFactor;

    offsetX = Math.round(offsetX);
    offsetY = Math.round(offsetY);

    editIndex = -1;
    text.style.display = "none";

    drawGrid();
}

canvas.addEventListener("wheel", (e) => {
    zoom(e);
});

canvas.addEventListener("mousedown", (e) => {
    currentButton = e.button;

    if (e.button == 1) {
        e.preventDefault();
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        canvas.style.cursor = "move";
    }
    if (currentButton == 0) {
        e.preventDefault();
        isDragging = true;
        isResizing = false;
        resizeDirection = "";
        startX = e.clientX;
        startY = e.clientY;
        for (let j = 0; j < boxes.length; j++) {
            boxes[j][7] = false;
            activeIndex = -1;
        }
        const x = e.clientX - getCanvasCoordinates().x;
        const y = e.clientY - getCanvasCoordinates().y;

        for (let i = boxes.length - 1; i >= 0 ; i--) {
            if (
                x >
                    (boxes[i][1] / standardSize) * tileSize +
                        offsetX -
                        4 -
                        5 &&
                x <
                    (boxes[i][1] / standardSize) * tileSize +
                        offsetX -
                        4 +
                        5 &&
                y >
                    (boxes[i][2] / standardSize) * tileSize +
                        offsetY -
                        4 -
                        5 &&
                y <
                    (boxes[i][2] / standardSize) * tileSize +
                        offsetY -
                        4 +
                        5
            ) {
                console.log("top left");
                resizeDirection = "top left";
                initialWidth = boxes[i][3];
                initialHeight = boxes[i][4];
                boxes[i][7] = true;
                activeIndex = i;
                isResizing = true;
                bstartX = (boxes[i][1] / standardSize) * tileSize;
                bstartY = (boxes[i][2] / standardSize) * tileSize;
                currentButton = 0;
                break;
            }
            if (
                x >
                    (boxes[i][1] / standardSize) * tileSize +
                        offsetX +
                        (boxes[i][3] / standardSize) * tileSize +
                        4 -
                        5 &&
                x <
                    (boxes[i][1] / standardSize) * tileSize +
                        offsetX +
                        (boxes[i][3] / standardSize) * tileSize +
                        4 +
                        5 &&
                y >
                    (boxes[i][2] / standardSize) * tileSize +
                        offsetY -
                        4 -
                        5 &&
                y <
                    (boxes[i][2] / standardSize) * tileSize +
                        offsetY -
                        4 +
                        5
            ) {
                console.log("top right");
                resizeDirection = "top right";
                initialWidth = boxes[i][3];
                initialHeight = boxes[i][4];
                boxes[i][7] = true;
                activeIndex = i;
                isResizing = true;
                bstartX = (boxes[i][1] / standardSize) * tileSize;
                bstartY = (boxes[i][2] / standardSize) * tileSize;
                currentButton = 0;
                break;
            }
            if (
                x >
                    (boxes[i][1] / standardSize) * tileSize +
                        offsetX -
                        4 -
                        5 &&
                x <
                    (boxes[i][1] / standardSize) * tileSize +
                        offsetX -
                        4 +
                        5 &&
                y >
                    (boxes[i][2] / standardSize) * tileSize +
                        offsetY +
                        (boxes[i][4] / standardSize) * tileSize +
                        4 -
                        5 &&
                y <
                    (boxes[i][2] / standardSize) * tileSize +
                        offsetY +
                        (boxes[i][4] / standardSize) * tileSize +
                        4 +
                        5
            ) {
                console.log("bottom left");
                resizeDirection = "bottom left";
                initialWidth = boxes[i][3];
                initialHeight = boxes[i][4];
                boxes[i][7] = true;
                activeIndex = i;
                isResizing = true;
                bstartX = (boxes[i][1] / standardSize) * tileSize;
                bstartY = (boxes[i][2] / standardSize) * tileSize;
                currentButton = 0;
                break;
            }
            if (
                x >
                    (boxes[i][1] / standardSize) * tileSize +
                        offsetX +
                        (boxes[i][3] / standardSize) * tileSize +
                        4 -
                        5 &&
                x <
                    (boxes[i][1] / standardSize) * tileSize +
                        offsetX +
                        (boxes[i][3] / standardSize) * tileSize +
                        4 +
                        5 &&
                y >
                    (boxes[i][2] / standardSize) * tileSize +
                        offsetY +
                        (boxes[i][4] / standardSize) * tileSize +
                        4 -
                        5 &&
                y <
                    (boxes[i][2] / standardSize) * tileSize +
                        offsetY +
                        (boxes[i][4] / standardSize) * tileSize +
                        4 +
                        5
            ) {
                console.log("bottom right");
                resizeDirection = "bottom right";
                initialWidth = boxes[i][3];
                initialHeight = boxes[i][4];
                bstartX = (boxes[i][1] / standardSize) * tileSize;
                bstartY = (boxes[i][2] / standardSize) * tileSize;
                boxes[i][7] = true;
                activeIndex = i;
                isResizing = true;
                console.log("YES IT IS WORKING")
                currentButton = 0;
                break;
            }
            if (
                x > (boxes[i][1] / standardSize) * tileSize + offsetX &&
                x <
                    (boxes[i][1] / standardSize) * tileSize +
                        offsetX +
                        (boxes[i][3] / standardSize) * tileSize &&
                y > (boxes[i][2] / standardSize) * tileSize + offsetY &&
                y <
                    (boxes[i][2] / standardSize) * tileSize +
                        offsetY +
                        (boxes[i][4] / standardSize) * tileSize
            ) {
                console.log("clicked", i);
                boxes[i][7] = true;
                if (i != editIndex) {
                    editIndex = -1;
                    text.style.display = "none";
                }
                bstartX = (boxes[i][1] / standardSize) * tileSize;
                bstartY = (boxes[i][2] / standardSize) * tileSize;
                activeIndex = i;
                drawGrid();
                break;
            }
        }
        if (activeIndex != editIndex) {
            editIndex = -1;
            text.style.display = "none";
        }
    }

    if (currentButton == 2) {
    }
});

canvas.addEventListener("mousemove", (e) => {
    if (currentButton == 1) {

        if (isDragging) {
            editIndex = -1;
            text.style.display = "none";

            offsetX += e.clientX - startX;
            offsetY += e.clientY - startY;
            startX = e.clientX;
            startY = e.clientY;
            drawGrid();
        }
    } else if (currentButton == 0) {
        console.log(isResizing);
        if (isResizing) {
            editIndex = -1;
            text.style.display = "none";
            if (resizeDirection == "top left") {

                let t1 = initialWidth - ((e.clientX - startX) * standardSize) / tileSize;
                let t2 = initialHeight - ((e.clientY - startY) * standardSize) / tileSize;
                if(t1 > 40 && t2 > 40){
                    boxes[activeIndex][3] = t1;
                    boxes[activeIndex][4] = t2;
                    boxes[activeIndex][1] = ((e.clientX - startX + bstartX) * standardSize) / tileSize;
                    boxes[activeIndex][2] = ((e.clientY - startY + bstartY) * standardSize) / tileSize;
                }
            } else if (resizeDirection == "top right") {

                let t1 = initialWidth + ((e.clientX - startX) * standardSize) / tileSize;
                let t2 = initialHeight - ((e.clientY - startY) * standardSize) / tileSize;
                if(t1 > 40 && t2 > 40){
                    boxes[activeIndex][3] = t1;
                    boxes[activeIndex][4] = t2;
                    boxes[activeIndex][2] = ((e.clientY - startY + bstartY) * standardSize) / tileSize;
                }
            } else if (resizeDirection == "bottom left") {

                let t1 = initialWidth - ((e.clientX - startX) * standardSize) / tileSize;
                let t2 = initialHeight + ((e.clientY - startY) * standardSize) / tileSize;
                if (t1 > 40 && t2 > 40) {
                    boxes[activeIndex][3] = t1;
                    boxes[activeIndex][4] = t2;
                    boxes[activeIndex][1] = ((e.clientX - startX + bstartX) * standardSize) / tileSize;
                }
            } else if (resizeDirection == "bottom right") {
                let t1 = initialWidth + ((e.clientX - startX) * standardSize) / tileSize;
                let t2 = initialHeight + ((e.clientY - startY) * standardSize) / tileSize;
                if (t1 > 40 && t2 > 40) {
                    boxes[activeIndex][3] = t1;
                    boxes[activeIndex][4] = t2;
                }
            }
            drawGrid();
        }
        else if (isDragging && activeIndex != -1 && !isResizing) {
            console.log("dragging");
            editIndex = -1;
            text.style.display = "none";
            boxes[activeIndex][1] =
                ((e.clientX - startX + bstartX) * standardSize) / tileSize;
            boxes[activeIndex][2] =
                ((e.clientY - startY + bstartY) * standardSize) / tileSize;
            drawGrid();
        }
    } else if (currentButton == 2) {
    }
});

canvas.addEventListener("contextmenu", (e) => {
    e.preventDefault();
});

canvas.addEventListener("dblclick", (e) => {
    if (e.button == 0) {
        const x = e.clientX - getCanvasCoordinates().x;
        const y = e.clientY - getCanvasCoordinates().y;

        for (let i = 0; i < boxes.length; i++) {
            if (
                x > (boxes[i][1] / standardSize) * tileSize + offsetX &&
                x <
                    (boxes[i][1] / standardSize) * tileSize +
                        offsetX +
                        (boxes[i][3] / standardSize) * tileSize &&
                y > (boxes[i][2] / standardSize) * tileSize + offsetY &&
                y <
                    (boxes[i][2] / standardSize) * tileSize +
                        offsetY +
                        (boxes[i][4] / standardSize) * tileSize
            ) {
                let removed = boxes.splice(i, 1);
                boxes.push(removed[0]);
                i = boxes.length - 1;
                drawGrid();
                editIndex = i;
                let tw = ((boxes[i][3] - 40) / standardSize) * tileSize;
                let th = (30 / standardSize) * tileSize;
                text.style.width = tw + "px";
                text.style.height = th + "px";
                text.style.fontSize = (18 / standardSize) * tileSize + "px";
                text.style.lineHeight = th + "px";
                //text.style.backgroundColor = boxes[i][5];

                text.style.left =
                    7 +
                    ((boxes[i][1] + boxes[i][3] / 2) / standardSize) *
                        tileSize +
                    offsetX -
                    tw / 2 +
                    "px";
                text.style.top =
                    7 +
                    ((boxes[i][2] + boxes[i][4] / 2) / standardSize) *
                        tileSize +
                    offsetY -
                    th / 2 +
                    "px";

                document.getElementById("text").value = boxes[i][6];
                text.style.display = "block";
                text.focus();
                text.setSelectionRange(text.value.length, text.value.length);
                break;
            }
        }
    }
});

document.addEventListener("mouseup", () => {
    isDragging = false;
    canvas.style.cursor = "default";
    currentButton = -1;
    activeIndex = -1;
    drawGrid();
});
