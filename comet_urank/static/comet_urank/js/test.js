var Test = (function() { 

	var a = 2;
	var b = 5;
	this.c = 10;

	var sum = function(){
		return a + b;
	};

	var add1toa = function(){
		a++; 
		return this;
	};
	var add1tob = function(){
		b++;
		return this;
	};

	var clear = function(){
		a=2;
		b=5;
		return this;
	}

	return {
		sum : sum,
		add1toa : add1toa,
		add1tob: add1tob,
		clear : clear
	}

})();