function context(canvasname, strokediv, nstrokediv, w,h) {

	var ccanvas = new chicharcanvas();
	
	ccanvas.init(canvasname, strokediv, nstrokediv, w, h);

	ccanvas.attachevents();

	var iterframe = function() {
		ccanvas.fiterstroke();
		return relaunchloop(true,iterframe);		
	}

	return iterframe;
}

startanim(context("chicharcanvas", "charstrokes", "charnstrokes", 750, 750));
