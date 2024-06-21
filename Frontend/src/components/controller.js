import {Arrow} from './arrow.js';

export class Controller {
    constructor(b1, d1, b2, d2) {
        this.b1 = b1;
        this.d1 = d1;
        this.points = [];
        this.b2 = null;
        this.d2 = null;

        this.mousestate = true;

        if (b2 != null && d2 != null) {
            this.b2 = b2;
            this.d2 = d2;
            this.mousestate = false;
        }

    }

    startArray(d1) {
        let points = [];
        let b1 = this.b1;
        if (d1 == "right") {
            points.push([b1.x + b1.width - 8, b1.y + b1.height / 2]);
            points.push([b1.x + b1.width + 20, b1.y + b1.height / 2]);
        }
        if (d1 == "left") {
            points.push([b1.x + 8, b1.y + b1.height / 2]);
            points.push([b1.x - 20, b1.y + b1.height / 2]);
        }
        if (d1 == "up") {
            points.push([b1.x + b1.width / 2, b1.y + 8]);
            points.push([b1.x + b1.width / 2, b1.y - 20]);
        }
        if (d1 == "down") {
            points.push([b1.x + b1.width / 2, b1.y + b1.height - 8]);
            points.push([b1.x + b1.width / 2, b1.y + b1.height + 20]);
        }
        return points;
    }
    
    endCoord(d2) {
        let b2 = this.b2;
        if (d2 == "right") {
            return [b2.x + b2.width - 8, b2.y + b2.height / 2];
        }
        if (d2 == "left") {
            return [b2.x + 8, b2.y + b2.height / 2];
        }
        if (d2 == "up") {
            return [b2.x + b2.width / 2, b2.y + 8];
        }
        if (d2 == "down") {
            return [b2.x + b2.width / 2, b2.y + b2.height - 8];
        }
        return [b2.x + b2.width / 2, b2.y + b2.height / 2];
    
    }

    endPoint(d2, mx, my) {
        let factor = 30;
        if(!this.mousestate) factor *= -1;
        if (d2 == "right") {
            return [mx - factor, my]
        }
        if (d2 == "left") {
            return [mx + factor, my]
        }
        if (d2 == "up") {
            return [mx, my + factor]
        }
        if (d2 == "down") {
            return [mx, my - factor]
        }
        return [mx,my];
    }

    distance(x1, y1, x2, y2) {
        return (x2 - x1) ** 2 + (y2 - y1) ** 2;
    }

    directionVector(x1, y1, x2, y2) {
        let h = 0;
        let v = 0;

        if (x1 < x2) h = "right";
        if (x1 > x2) h = "left";

        if (y1 < y2) v = "down";
        if (y1 > y2) v = "up";

        return [h, v];
    }

    directiondistance(d1, d2) {
        let directions = ["up","right","down","left"];
        let x = Math.abs(directions.indexOf(d2) - directions.indexOf(d1));
        if (x == 3) return 1;
        return x;
    }

    checkDirection(mx,my) {
        var d1 = this.distance(this.b1.x, this.b1.y + this.b1.height / 2, mx, my);
        var d2 = this.distance(this.b1.x + this.b1.width, this.b1.y + this.b1.height / 2, mx, my);
        var d3 = this.distance(this.b1.x + this.b1.width / 2, this.b1.y, mx, my);
        var d4 = this.distance(this.b1.x + this.b1.width / 2, this.b1.y + this.b1.height, mx, my);

        var min = Math.min(d1, d2, d3, d4);

        if(min == d1) return "left";
        if(min == d2) return "right";
        if(min == d3) return "up";
        if(min == d4) return "down";
    }

    render(ctx,mx,my) {
        let d2;
        if(this.mousestate) {
            d2 = "left"
        }
        else {
            d2 = this.d2;
            [mx,my] = this.endCoord(d2);
        }

        let d1 = this.d1;
        let p1 = this.startArray(d1);
        let v;
        let testx;
        let testy;
        let testd;
        let t1;
        let t2;
        let diff;
        let move;
        let e = this.endPoint(d2, mx, my);
        let ex = e[0];
        let ey = e[1];
        let mdbreak = 0;
        let initialdirection = this.directionVector(p1[1][0], p1[1][1], ex, ey);
        let limit = 2;
        let inversion = 0;
        let iV = [0,0,0,0];
        let lv = [2,2,2,2];
        let tempd = d2;

        if(this.mousestate) {
            if(tempd == "right") tempd = "left";
            if(tempd == "left") tempd = "right";
            if(tempd == "up") tempd = "down";
            if(tempd == "down") tempd = "up";
        }


        if(d1 == "right" && tempd == "right") iV = [-1,-1,1,1], lv = [1,1,1,1];
        if(d1 == "right" && tempd == "left") iV = [-1,-1,-1,-1], lv = [2,2,2,2];
        if(d1 == "right" && tempd == "up") iV = [1,1,1,1], lv = [2,1,1,1];
        if(d1 == "right" && tempd == "down") iV = [1,1,1,1], lv = [1,2,2,1];
        if(d1 == "left" && tempd == "right") iV = [-1,-1,-1,-1], lv = [2,2,2,2];
        if(d1 == "left" && tempd == "left") iV = [-1,-1,1,1], lv = [1,1,1,1];
        if(d1 == "left" && tempd == "up") iV = [1,1,1,1], lv = [1,2,2,1];
        if(d1 == "left" && tempd == "down") iV = [1,1,1,1], lv = [2,1,1,2];
        if(d1 == "up" && tempd == "right") iV = [1,1,1,1], lv = [2,1,1,1];
        if(d1 == "up" && tempd == "left") iV = [1,1,1,1], lv = [1,2,2,1];
        if(d1 == "up" && tempd == "up") iV = [-1,-1,1,1], lv = [1,1,1,1];
        if(d1 == "up" && tempd == "down") iV = [-1,-1,-1,-1], lv = [2,2,2,2];
        if(d1 == "down" && tempd == "right") iV = [1,1,1,1], lv = [1,2,2,1];
        if(d1 == "down" && tempd == "left") iV = [1,1,1,1], lv = [2,1,1,2];
        if(d1 == "down" && tempd == "up") iV = [-1,-1,-1,-1], lv = [2,2,2,2];
        if(d1 == "down" && tempd == "down") iV = [-1,-1,1,1], lv = [1,1,1,1];

        if(initialdirection[0] == "right" && initialdirection[1] == "up") {inversion = iV[0], limit = lv[0]};
            if(initialdirection[0] == "right" && initialdirection[1] == "down") {inversion = iV[1], limit = lv[1]};
            if(initialdirection[0] == "left" && initialdirection[1] == "up") {inversion = iV[2], limit = lv[2]};
            if(initialdirection[0] == "left" && initialdirection[1] == "down") {inversion = iV[3], limit = lv[3]};
        

        testx = p1[1][0];
        testy = p1[1][1];
        testd = d1;
        let prev;
        for(let i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) {
            v = this.directionVector(testx, testy, ex,ey);
            diff = this.directiondistance(testd,d2);
    
            t1 = this.directiondistance(v[0],d2);
            t2 = this.directiondistance(v[1],d2);

            if(inversion) {
                t1 = this.directiondistance(v[0],testd);
                t2 = this.directiondistance(v[1],testd);
            }


            if(t1 < t2) testd = v[0];
            else if(t2 < t1) testd = v[1];
            else testd = v[0];

            
            if(prev != null) {
                if(mdbreak < limit) {
                    if(v[1] == prev) testd = v[0];
                    else if(v[0] == prev) testd = v[1];
                }
                else {
                    if(v[1] == prev) testd = v[1];
                    else if(v[0] == prev) testd = v[0];
                }
            }

            prev = testd;
    
            if(testd == "down") {
                testy = ((ey - testy) / 2) + testy;
                p1.push([testx, testy]);
                mdbreak++;
            }
            if(testd == "up") {
                testy = ((ey - testy) / 2) + testy;
                p1.push([testx, testy]);
                mdbreak++;
            }
            if(testd == "right") {
                testx = ((ex - testx) / 2) + testx;
                p1.push([testx, testy]);
                mdbreak++;
            }
            if(testd == "left") {
                testx = ((ex - testx) / 2) + testx;
                p1.push([testx, testy]);
                mdbreak++;
            }
        }
        p1.push([ex,ey]);
        p1.push([mx,my]);
        let d3 = "";
        if(d1 == "right") d3 = "left";
        if(d1 == "left") d3 = "right";
        if(d1 == "up") d3 = "down";
        if(d1 == "down") d3 = "up";

        if(!this.mousestate) {
            if(this.d2 == "right") d2 = "left";
            if(this.d2 == "left") d2 = "right";
            if(this.d2 == "up") d2 = "down";
            if(this.d2 == "down") d2 = "up";
        }
        Arrow(ctx, p1, null, d2);
    }
}