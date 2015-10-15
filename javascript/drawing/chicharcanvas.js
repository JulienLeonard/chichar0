
function chicharcanvas() {
	this.canvasframe = null;
	this.canvas = null;
	this.viewviewbox = [-10.0,-10.0, 10.0,10.0];
	this.background = Color.prototype.white();
	this.savecoords    = null;
	this.coordindex    = null;
	this.currentstroke = null;
	this.chichar       = null;
}

//
// must return a function to iterframe
//
chicharcanvas.prototype.init = function(canvasname,strokediv, nstrokediv, w,h,isactive) {
	console.log("chicharcanvas.prototype.init this " + this + " this.canvasframe " + this.canvasframe);

	this.canvas = initcanvas(canvasname,w,h,this.background);

	resetviewbox(this.canvas,this.viewviewbox);

	this.canvasframe = canvasitem(canvasname);

	this.strokediv  = strokediv;
	this.nstrokediv = nstrokediv;
};

chicharcanvas.prototype.fiterstroke = function() {

	resetviewbox(this.canvas,this.viewviewbox);

	if (this.chichar == null && this.savecoords == null) {
		var scoords = document.getElementsByName(this.strokediv)[0].value;
		console.log("scoords" + scoords.length);
		if (scoords != null && scoords.length > 0) {
			this.savecoords     = scoords.split(",");
			this.coordindex = 0;
		}
	}

	if (this.savecoords != null && this.coordindex < this.savecoords.length) {
		if (this.savecoords[this.coordindex] == ";") {
			this.coordindex += 2;
		}
		p = new Point(this.savecoords[this.coordindex],this.savecoords[this.coordindex+1]);
		chidrawcircle(this.canvas,p.x, p.y);
		this.coordindex += 2;
	}

};


chicharcanvas.prototype.ftouchdowndrawcircle = function(e) {
	console.log("trigger touchdowndrawcircle this " + this + " canvaframe " + this.canvasframe);
	this.savecoords = null;
	
	if (this.chichar == null) {
		this.chichar = new Chichar();
		this.currentstroke = null;
	}

	var p = getcenteredcoords(this.canvasframe,e)
	chidrawcircle(this.canvas,p.x, p.y);
	
	this.currentstroke = new Stroke();
	this.currentstroke.points.push(p);
	e.preventDefault();
};


chicharcanvas.prototype.ftouchupdrawcircle = function(e) {
	this.chichar.strokes.push(this.currentstroke);
		
	document.getElementsByName(this.nstrokediv)[0].value = this.chichar.strokes.length;
		
	var lcoords = [];
	for (var i = 0; i < this.chichar.strokes.length; i++) {
		var stroke = this.chichar.strokes[i];
		for (var j = 0; j < stroke.points.length; j++) {
			lcoords.push(stroke.points[j].x);
			lcoords.push(stroke.points[j].y);
		}
		lcoords.push(";,;");
	}
	var sstrokes = lcoords.join(',');
	
	document.getElementsByName(this.strokediv)[0].value = sstrokes;
	
	this.currentstroke = null;
};


chicharcanvas.prototype.fmovedrawcircle = function(e) {
	if (this.currentstroke) {
		var p = getcenteredcoords(this.canvasframe,e)
		chidrawcircle(this.canvas,p.x, p.y);
		this.currentstroke.points.push(p)
	}
	e.preventDefault();
};



chicharcanvas.prototype.attachevents = function(cccanvas) {
	console.log("attachevents cccanvas " + this + " canvas " + this.canvas + " canvasframe " + this.canvasframe);

	bindcanvas(this.canvasframe, "mousedown", this.ftouchdowndrawcircle.bind(this), false);
	bindcanvas(this.canvasframe, "mousemove", this.fmovedrawcircle.bind(this),      false);
	bindcanvas(this.canvasframe, "mouseup",   this.ftouchupdrawcircle.bind(this),   false);

	bindcanvas(this.canvasframe, "touchstart",this.ftouchdowndrawcircle.bind(this), false);
	bindcanvas(this.canvasframe, "touchmove", this.fmovedrawcircle.bind(this),      false);
	bindcanvas(this.canvasframe, "touchend",  this.ftouchupdrawcircle.bind(this),   false);
}

