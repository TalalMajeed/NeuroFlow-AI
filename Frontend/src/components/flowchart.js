import { Box } from './box.js';
import { Arrow } from './arrow.js';
import {Controller} from './controller.js';

export let offsetX = 0;
export let offsetY = 0;

function getCanvasCoordinates(canvas) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: rect.left + window.scrollX,
        y: rect.top + window.scrollY,
    };
}


export class Flowchart {
    setData(data) {
        this.tempBoxes = [];

        for(let i=0; i < data.length; i++) {
            let temp = data[i];
            let color = temp.pop();
            this.tempBoxes.push(new Box(0,0,temp,color));
        }

        let dim = [];

        for(let i=0; i < this.tempBoxes.length; i++) {
            dim.push(this.tempBoxes[i].retrieveDim());
        }
        return dim;
    }
    setRender(data,connections) {
        this.boxes = [];
        this.controllers = [];
        for(let i=0; i < this.tempBoxes.length; i++) {
            let t = this.tempBoxes[i];
            t.setPos(data[i][0],data[i][1]);
            this.boxes.push(t);
        }
        for(let i=0; i < connections.length; i++) {
            let c = connections[i];
            this.controllers.push(new Controller(this.boxes[c[0]],c[2],this.boxes[c[1]],c[3]));
        }
        this.tempBoxes = [];

        this.drawGrid();

    }
    getFlowState() {
        let boxes = [];

        for(let i=0; i < this.boxes.length; i++) {
            let box = this.boxes[i];
            boxes.push([box.x,box.y,box.data,box.colorString]);
        }

        let connections = [];

        for(let i=0; i < this.controllers.length; i++) {
            let c = this.controllers[i];
            connections.push([this.boxes.indexOf(c.b1),this.boxes.indexOf(c.b2),c.d1,c.d2]);
        }

        return [boxes,connections];
    }

    setFlowState(data) {
        this.boxes = [];
        this.controllers = [];
        for(let i=0; i < data[0].length; i++) {
            let d = data[0][i];
            let b = new Box(d[0],d[1],d[2],d[3]);
            this.boxes.push(b);
        }
        for(let i=0; i < data[1].length; i++) {
            let c = data[1][i];
            let b1 = this.boxes[c[0]];
            let b2 = this.boxes[c[1]];
            this.controllers.push(new Controller(b1,c[2],b2,c[3]));
        }
        this.drawGrid();
    }
    constructor(id) {
        this.canvas = document.querySelector("#main-canvas");
        this.ctx = this.canvas.getContext("2d");
        this.text = document.querySelector("#text");
        this.drawLines = true;
        
        this.canvasWidth = this.canvas.width;
        this.canvasHeight = this.canvas.height;
        this.tileSize = 40;
        
        this.standardSize = 40;
        this.boxes = [];
        this.controllers = [];
        this.tempBoxes = [];
        this.cursorShift = true;


        this.drawGrid();

        let isDragging = false;
        let startX = 0;
        let startY = 0;
        let currentButton = -1;
        let isResizing = false;
        let isMoving = false;
        let side = 0;
        this.activeIndex = -1;

        this.canvas.addEventListener("mousedown", (e) => {
            currentButton = e.button;

            if(!isDragging && this.activeIndex != -1) {
                    side = this.boxes[this.activeIndex].selectTest(e.clientX - getCanvasCoordinates(this.canvas).x, e.clientY - getCanvasCoordinates(this.canvas).y)
                    startX = e.clientX;
                    startY = e.clientY;
                    if(side == 1) {
                        isResizing = true;

                    };
                    if(side == 2) {
                        isResizing = true;
                    };
                    if(side == 3) {
                        isResizing = true;
                    };
                    if(side == 4) {
                        isResizing = true;
                    };
            }

            if(!isDragging && !isResizing) {
                for (let i = 0; i < this.boxes.length; i++) {
                    if(this.boxes[i].innerSelectTest(e.clientX - getCanvasCoordinates(this.canvas).x, e.clientY - getCanvasCoordinates(this.canvas).y)) {
                        isMoving = true;
                        startX = e.clientX;
                        startY = e.clientY;
                        break;
                    };
                }
            }

            if (this.cursorShift) {
                e.preventDefault();
                isDragging = true;
                startX = e.clientX;
                startY = e.clientY;
                this.canvas.style.cursor = "move";
            }
            if (!this.cursorShift) {
                if(!isDragging && !isResizing && !isMoving) {
                    this.activeIndex = -1;
                    this.canvas.style.cursor = "default";
                }

                for (let i = 0; i < this.boxes.length; i++) {
                    if(this.boxes[i].innerSelectTest(e.clientX - getCanvasCoordinates(this.canvas).x, e.clientY - getCanvasCoordinates(this.canvas).y)) {
                        this.activeIndex = i;
                        break;
                    };
                }
            }

        });

        this.canvas.addEventListener("mousemove", (e) => {
            if(isMoving && !isDragging && !this.cursorShift) {
                this.boxes[this.activeIndex].shift(e.clientX - startX, e.clientY - startY);
            }   
            if(isResizing && !isDragging && this.activeIndex != -1) {
                if(side == 4) {
                    this.boxes[this.activeIndex].resize4(e.clientX - startX, e.clientY - startY);
                }
                if(side == 1) {
                    this.boxes[this.activeIndex].resize1(e.clientX - startX, e.clientY - startY);
                }
                if(side == 2) {
                    this.boxes[this.activeIndex].resize2(e.clientX - startX, e.clientY - startY);
                }
                if(side == 3) {
                    this.boxes[this.activeIndex].resize3(e.clientX - startX, e.clientY - startY);
                }
            }
            if(!isDragging && this.activeIndex != -1 && !this.cursorShift) {
                let flag = false;
                if(this.boxes[this.activeIndex].selectTest(e.clientX - getCanvasCoordinates(this.canvas).x, e.clientY - getCanvasCoordinates(this.canvas).y) != -1) {
                    flag = true;
                };

                if(flag) {
                    this.canvas.style.cursor = "pointer";
                }
                else {
                    this.canvas.style.cursor = "default";
                }
            }

            if (this.cursorShift) {
                if (isDragging) {
                    offsetX += e.clientX - startX;
                    offsetY += e.clientY - startY;
                    startX = e.clientX;
                    startY = e.clientY;
                }
            }
            
            this.drawGrid();

        });

        this.canvas.addEventListener("contextmenu", (e) => {
            e.preventDefault();
        });

        document.addEventListener("mouseup", (e) => {
            for(let i = 0; i < this.boxes.length; i++) {
                this.boxes[i].setInitial();
            }
            isDragging = false;
            isResizing = false;
            isMoving = false;
            this.drawGrid();
            //Set the cursor back to default
            this.canvas.style.cursor = "default";

        });
    }

    drawGrid() {
        let ctx = this.ctx;
        let canvas = this.canvas;
        let canvasWidth = this.canvasWidth;
        let canvasHeight = this.canvasHeight;
        let tileSize = this.tileSize;
        ctx.strokeStyle = "#ccc";
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        ctx.beginPath();

        if(this.drawLines) {
            let i = 0;
            for (
                i = offsetX % tileSize;
                i < this.canvasWidth + tileSize * 2;
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
        }



        ctx.closePath();

        for(let i=0; i < this.controllers.length; i++) {
            this.controllers[i].render(ctx);
        }

        for (let i = 0; i < this.boxes.length; i++) {
            if(this.activeIndex == i) {
                this.boxes[i].renderSelector(ctx);
            }
            this.boxes[i].renderShape(ctx);
            this.boxes[i].renderText(ctx);
        }
    }

    resizeCanvas(w,h) {
        this.canvas.style.width = w + "px";
        this.canvas.style.height = h + "px";
        this.canvas.width = w;
        this.canvas.height = h;
        this.canvasWidth = w;
        this.canvasHeight = h;
        this.drawGrid();

    }
}