var canvasname    = "chicharcanvas";
var canvas        = null;
var mycanvasitem    = null;

function Chichar() {
	this.strokes = [];
}

function Stroke() {
	this.points = []
}


function chidrawcircle(canvas,x,y) {
	drawcircle(canvas,circle(x,y,1.0),Color.prototype.black(0.1));
}

function context() {

	var w = 750,
		h = 750,
	    background = Color.prototype.white();
	

	canvas = initcanvas(canvasname,w,h,background);

	viewviewbox = [-10.0,-10.0, 10.0,10.0];

	resetviewbox(canvas,viewviewbox);

	mycanvasitem = canvasitem(canvasname);

	chichar = new Chichar();

	currentstroke = null;
	
	var getcenteredcoords = function(e) {
		var rect = mycanvasitem.getBoundingClientRect();
		var mouseX = e.clientX - rect.left;
        var mouseY = e.clientY - rect.top;
        var x =   (mouseX / mycanvasitem.width) * 2 - 1;
        var y = - (mouseY / mycanvasitem.height) * 2 + 1;
		return new Point(x,y);
	}

	var touchdowndrawcircle = function(e) {
		p = getcenteredcoords(e)
		chidrawcircle(canvas,p.x * 10.0, p.y * 10.0);
		currentstroke = new Stroke();
		currentstroke.points.push(p)
	};

	var touchupdrawcircle = function(e) {
		chichar.strokes.push(currentstroke);
		currentstroke = null;
	};

	var movedrawcircle = function(e) {
		if (currentstroke) {
			p = getcenteredcoords(e)
			chidrawcircle(canvas,p.x * 10.0, p.y * 10.0);
			currentstroke.points.push(p)
		}
	};



	bindcanvas(mycanvasitem,"mousedown",touchdowndrawcircle, false);
	bindcanvas(mycanvasitem,"mousemove",movedrawcircle,      false);
	bindcanvas(mycanvasitem,"mouseup",  touchupdrawcircle,   false);

	bindcanvas(mycanvasitem,"touchstart",touchdowndrawcircle, false);
	bindcanvas(mycanvasitem,"touchmove", movedrawcircle,      false);
	bindcanvas(mycanvasitem,"touchend",  touchupdrawcircle,   false);


	function iterframe() {

		viewviewbox = [-10.0,-10.0, 10.0,10.0];

		resetviewbox(canvas,viewviewbox);

		return relaunchloop(true,iterframe);		
	}

	return iterframe;
}

startanim(context());
