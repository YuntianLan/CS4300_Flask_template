var returnDict = {
	"group0": 0,
	"group1": 0,
	"group2": 0,
	"group3": 0,
	"group4": 0,
	"group5": 0,
	"group6": 0,
	"group7": 0,
	"group8": 0,
	"group9": 0,
};

// When user clicks a value to agree/disagree with the prompt, display to the user what they selected
$('.option').mousedown(function () {
	var classList = $(this).attr('class');
	// console.log(classList);
	var classArr = classList.split(" ");
	// console.log(classArr);
	var this_group = classArr[0];
	var value = parseInt(classArr[classArr.length-1]);
	//console.log(this_group);

	// If button is already selected, de-select it when clicked and subtract any previously added values to the total
	// Otherwise, de-select any selected buttons in group and select the one just clicked
	if($(this).hasClass('active')) {
		$(this).removeClass('active');
	} else {
		 //$('class='thisgroup).prop('checked', false);
		 //console.log($('.'+this_group+'.active').text());
		$('.'+this_group).removeClass('active');
		returnDict[this_group] = value;

		 //$(this).prop('checked', true);
		$(this).addClass('active');
	}

	console.log(Object.values(returnDict)); // THIS IS WHAT WE WANT TO PASS TO THE BACKEND!!
});

$.ajax({
	type: "GET",
	contentType: "application/json",
	url: "/",
	data: JSON.stringify(returnDict),
	dataType: "json",
	success: function(response) {
		console.log(response);
	},
	error: function(err) {
		console.log(err);
	}
});


$('#submit-btn').click(function () {

	document.data = returnDict;
	var catchphrace = $('#catchphrase').val();
	var adj = $('#adjectives').val();
	var moviename = $('#moviename').val();
	var character = $('#charactername').val();

	var hpchecked = document.getElementById("hpchecked");
	var gotchecked = document.getElementById("gotchecked");
	var marvelchecked = document.getElementById("marvelchecked");
	var swchecked = document.getElementById("swchecked");

	var url = "result?group0=" + returnDict["group0"] + 
			"&group1=" + returnDict["group1"] + 
			"&group2=" + returnDict["group2"] + 
			"&group3=" + returnDict["group3"] + 
			"&group4=" + returnDict["group4"] + 
			"&group5=" + returnDict["group5"] + 
			"&group6=" + returnDict["group6"] + 
			"&group7=" + returnDict["group7"] + 
			"&group8=" + returnDict["group8"] + 
			"&group9=" + returnDict["group9"] +
			"&catchphrace=" + catchphrace +
			"&adj="+ adj +
			"&moviename=" + moviename +
			"&character=" +character +
			"hp=" + hpchecked + 
			"got" + gotchecked +
			"mar" + marvelchecked +
			"sw" + swchecked
			;
	document.location.href = url;


});

// Refresh the screen to show a new quiz if they click the retake quiz button
$('#retake-btn').click(function () {
	document.location.href = "/search";
});

$('#home-btn').click(function () {
	document.location.href = "/";
});

