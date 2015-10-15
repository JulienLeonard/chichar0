

function Chichar() {
	this.strokes = [];
}

function Stroke() {
	this.points = []
}


function chidrawcircle(canvas,x,y) {
	console.log("chidrawcircle" + x + y);
	drawcircle(canvas,circle(x,y,0.05),Color.prototype.black(0.1));
}
