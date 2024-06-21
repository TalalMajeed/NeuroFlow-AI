import { offsetX, offsetY } from "./flowchart.js";

export function Arrow(ctx,points, head1direction, head2direction) {
    function drawLine(point1, point2) {
        ctx.strokeStyle = "#000";
        ctx.beginPath();
        ctx.moveTo(point1[0], point1[1]);
        ctx.lineTo(point2[0], point2[1]);
        ctx.stroke();
    }
    function drawArrowhead(point, d) {
        let direction = 0;
        if(d == null) return;
        if(d == "right") direction = 0;
        if(d == "left") direction = Math.PI;
        if(d == "up") direction = Math.PI * 1.5;
        if(d == "down") direction = Math.PI / 2;
        var arrowLength = 10;
        var arrowWidth = 15;

        //Set Stroke Color
        ctx.fillStyle = "#000";
        ctx.strokeStyle = "#000";
        ctx.lineWidth = 2;
        ctx.save();
        ctx.translate(point[0], point[1]);
        ctx.rotate(direction);
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(-arrowLength, arrowWidth / 2);
        ctx.lineTo(-arrowLength, -arrowWidth / 2);
        ctx.closePath();
        ctx.stroke();
        ctx.fill();
        ctx.restore();
        ctx.lineWidth = 1;
    }
    for (var i = 0; i < points.length - 1; i++) {
        drawLine([points[i][0] + offsetX,points[i][1] + offsetY], [points[i+1][0] + offsetX,points[i+1][1] + offsetY]);
    }
    if (head1direction !== null) {
        drawArrowhead([point[0][0] + offsetX, point[0][1] + offsetY], head1direction);
    }
    if (head2direction !== null) {
        drawArrowhead([points[points.length - 1][0] + offsetX, points[points.length - 1][1] + offsetY], head2direction);
    }
}