function flattenArray(arr) {
    return arr.reduce(function(flat, toFlatten) {
        return flat.concat(Array.isArray(toFlatten) ? flattenArray(toFlatten) : toFlatten);
    }, []);
}

function calculateLines(data) {
    let totalLines = 0;

    for (let i = 0; i < data.length; i++) {
        const words = data[i].split(' ');
        let currentLines = 0;
        let currentLineLength = 0;
        for (let j = 0; j < words.length; j++) {
            currentLineLength += words[j].length + 1;
            if (currentLineLength > 30) {
                currentLines++;
                currentLineLength = words[j].length + 1;
            }
        }
        if (currentLineLength > 0) {
            currentLines++;
        }
        totalLines += currentLines;
    }

    return totalLines;
}

import { offsetX, offsetY } from "./flowchart.js";


export class Box {
    constructor(x,y,data,color) {
        this.x = x;
        this.y = y;
        this.width = 150;
        this.height = 50;
        this.data = flattenArray(data);
        this.color = "#919191";
        this.textColor = "#fff";
        this.wi = this.width;
        this.hi = this.height;
        this.xi = x;
        this.yi = y;
        this.fontSize= 14;
        this.shape = "rectangle";
        this.minWidth = 0;
        this.minHeight = 0;
        this.colorString = color;
        this.setDim();

        if(color == "important") {
            this.color = "#e8b02c";
        }
        if(color == "testing") {
            this.color = "#46b98a";
        }
        if(color == "setup") {
            this.color = "#46b98a";
        }
    }

    renderShape(ctx) {
        ctx.fillStyle = this.color;
        if(this.shape === "rectangle") {
        ctx.fillRect(this.x + offsetX + 8, this.y + offsetY + 8, this.width - 16, this.height - 16);
        }
        if(this.shape === "parallelogram") {
            ctx.beginPath();
            ctx.moveTo(this.x + offsetX + this.height * 0.1 + 20, this.y + offsetY + 8);
            ctx.lineTo(this.x + offsetX + this.width - 8, this.y + offsetY + 8);
            ctx.lineTo(this.x + offsetX + this.width - this.height * 0.1 - 20, this.y + offsetY + this.height - 8);
            ctx.lineTo(this.x + offsetX + 8, this.y + offsetY + this.height - 8);
            ctx.closePath();
            ctx.fill();
        }
    }

    renderText(ctx) {
        const centerX = this.x;
        const centerY = this.y + offsetY + (this.height / 2);
    
        let titleHeight = 0;
    
        for (let i = 0; i < this.data.length; i++) {
            let sub = [];
            ctx.font = this.fontSize + "px Arial";
            if (i === 0) {

                ctx.font = "bold " + ctx.font;
                ctx.fillStyle = "#fff";
            } else {
                ctx.fillStyle = "#fff";
            }
    
            sub = this.data[i];
            let textWidth = 0;
            let maxWidth = 0;

            if(this.shape === "rectangle") {
                textWidth = -25;
                maxWidth = this.width - 40; 
            }
            if(this.shape === "parallelogram") {
                textWidth = -55;
                maxWidth = this.width - 100; 
            }
    

            const textHeight = this.fontSize / 2;
            const textX = centerX - textWidth + offsetX;
            let textY = centerY - (this.data.length * this.fontSize / 1.7) + (i * this.fontSize * 1.5);
    
            if (i !== 0) {
                textY += titleHeight * 0.5;
            }

            const words = sub.split(' ');
            let line = '';
            let lines = [];
            for (let j = 0; j < words.length; j++) {
                const testLine = line + words[j] + ' ';
                const metrics = ctx.measureText(testLine);
                const testWidth = metrics.width;
                if (testWidth > maxWidth && j > 0) {
                    lines.push(line);
                    line = words[j] + ' ';
                    textY -= 15;
                } else {
                    line = testLine;
                }
            }
            lines.push(line);
    
            if (i === 0) {
                titleHeight = lines.length * (this.fontSize * 1);
            }
    
            lines.forEach((line, index) => {
                if (i === 0) {
                    ctx.fillText(line.trim(), textX, textY + (index * this.fontSize * 1.5));
                } else {
                    ctx.fillText("• " + line.trim(), textX, textY + (index * this.fontSize * 1.5));
                }
            });
        }
    }
    

    

    setDim() {
        let longest = 0;
        for (let i = 0; i < this.data.length; i++) {
            if (this.data[i].length > longest) {
                longest = this.data[i].length;
            }
        }
        if(longest > 30) {
            longest = 30;
        }
        let totalLines = calculateLines(this.data);
        this.width = longest * 8 + 100;
        this.height = totalLines * 20 + 80;

        this.wi = this.width;
        this.hi = this.height;
        this.minWidth = this.width;
        this.minHeight = this.height - 20;
        console.log()
    }

    retrieveDim() {
        return [this.width, this.height];
    }

    setPos(x,y) {
        this.x = x;
        this.y = y;
        this.xi = x;
        this.yi = y;
    }

    renderSelector(ctx) {
        ctx.strokeStyle = "#347deb";
        ctx.lineWidth = 1;
        ctx.strokeRect(this.x + offsetX, this.y + offsetY, this.width, this.height);
        ctx.fillStyle = "#fff";
        ctx.beginPath();
        ctx.arc(this.x + offsetX, this.y + offsetY, 7, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(this.x + this.width + offsetX, this.y + offsetY, 7, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(this.x + offsetX, this.y + this.height + offsetY, 7, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(this.x + this.width + offsetX, this.y + this.height + offsetY, 7, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = "#000";
        ctx.beginPath();
        ctx.strokeRect(this.x + offsetX + this.width / 2 -3.5, this.y + offsetY - 15, 7, 7);
        ctx.fill();
        ctx.stroke();
        ctx.beginPath();
        ctx.strokeRect(this.x + offsetX + this.width / 2 - 3.5, this.y + offsetY + this.height + 8, 7, 7);
        ctx.fill();
        ctx.stroke();
        ctx.beginPath();
        ctx.strokeRect(this.x + offsetX - 15, this.y + offsetY + this.height / 2 - 3.5, 7, 7);
        ctx.fill();
        ctx.stroke();
        ctx.beginPath();
        ctx.strokeRect(this.x + offsetX + this.width + 8, this.y + offsetY + this.height / 2 - 3.5, 7, 7);
        ctx.fill();
        ctx.stroke();
    }

    selectTest(mx,my) {
        if (mx > this.x + offsetX - 7 && mx < this.x + offsetX + 7 && my > this.y + offsetY - 7 && my < this.y + offsetY + 7) {
            return 1;
        } else if (mx > this.x + this.width + offsetX - 7 && mx < this.x + this.width + offsetX + 7 && my > this.y + offsetY - 7 && my < this.y + offsetY + 7) {
            return 2;
        } else if (mx > this.x + offsetX - 7 && mx < this.x + offsetX + 7 && my > this.y + this.height + offsetY - 7 && my < this.y + this.height + offsetY + 7) {
            return 3;
        } else if (mx > this.x + this.width + offsetX - 7 && mx < this.x + this.width + offsetX + 7 && my > this.y + this.height + offsetY - 7 && my < this.y + this.height + offsetY + 7) {
            return 4;
        }
        else if (mx > this.x + offsetX + this.width / 2 - 7 && mx < this.x + offsetX + this.width / 2 + 7 && my > this.y + offsetY - 15 && my < this.y + offsetY - 8) {
            return 5;
        } else if (mx > this.x + offsetX + this.width / 2 - 7 && mx < this.x + offsetX + this.width / 2 + 7 && my > this.y + offsetY + this.height + 8 && my < this.y + offsetY + this.height + 15) {
            return 6;
        } else if (mx > this.x + offsetX - 15 && mx < this.x + offsetX - 8 && my > this.y + offsetY + this.height / 2 - 7 && my < this.y + offsetY + this.height / 2 + 7) {
            return 7;
        } else if (mx > this.x + offsetX + this.width + 8 && mx < this.x + offsetX + this.width + 15 && my > this.y + offsetY + this.height / 2 - 7 && my < this.y + offsetY + this.height / 2 + 7) {
            return 8;
        }
        else {
            return -1;
        }
    }

    innerSelectTest(mx,my) {
        if (mx > this.x + offsetX && mx < this.x + this.width + offsetX && my > this.y + offsetY && my < this.y + this.height + offsetY) {
            return true;
        } else {
            return false;
        }
    }

    setInitial() {
        this.wi = this.width;
        this.hi = this.height;
        this.xi = this.x;
        this.yi = this.y;
    }

    resize4(x,y) {
        if(this.wi + x >= this.minWidth) {
            this.width = this.wi + x;
        }
        if(this.hi + y >= this.minHeight) {
            this.height = this.hi + y;
        }

    }

    resize1(x,y) {
        if(this.wi - x >= this.minWidth) {
            this.x = x + this.xi;
            this.width = this.wi - x;
        }
        if(this.hi - y >= this.minHeight) {
            this.height = this.hi - y;
            this.y = y + this.yi;
        }

    }

    resize2(x, y) {
        //Top right corner
        if(this.wi + x >= this.minWidth) {
            this.width = this.wi + x;
        }
        if(this.hi - y >= this.minHeight) {
            this.height = this.hi - y;
            this.y = y + this.yi;
        }
    }
    
    resize3(x, y) {
        //Bottom left corner
        if(this.wi - x >= this.minWidth) {
            this.x = x + this.xi;
            this.width = this.wi - x;
        }
        if(this.hi + y >= this.minHeight) {
            this.height = this.hi + y;
        }
    }

    shift(x,y) {
        this.x = this.xi + x;
        this.y = this.yi + y;
    }
}