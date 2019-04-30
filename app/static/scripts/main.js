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
	var num_group = parseInt(this_group[this_group.length-1])
	var value = parseInt(classArr[classArr.length-1]);
	var next_id = 'question' + (num_group+1).toString()
	//console.log(this_group);

	// If button is already selected, de-select it when clicked and subtract any previously added values to the total
	// Otherwise, de-select any selected buttons in group and select the one just clicke
	if($(this).hasClass('active')) {
		$(this).removeClass('active');
	} else {
		 //$('class='thisgroup).prop('checked', false);
		 //console.log($('.'+this_group+'.active').text());
		$('.'+this_group).removeClass('active');
		returnDict[this_group] = value;

		 //$(this).prop('checked', true);
		$(this).addClass('active');
		if (next_id < 10){
			document.getElementById(next_id).scrollIntoView({block: 'start', behavior: 'smooth'});
		}
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

var countries1 = ['Anthony Goldstein in Harry Potter', 'Xenophilius Lovegood in Harry Potter', 'Newt Scamander in Harry Potter', 'Jacob Kowalski in Harry Potter', 'Katie Bell in Harry Potter', 'Ginny Weasley in Harry Potter', 'Ignotus Peverell in Harry Potter', 'Hermione Granger in Harry Potter', 'Dean Thomas in Harry Potter', 'Ernie Macmillan in Harry Potter', 'Auntie Muriel in Harry Potter', 'Cuthbert Binns in Harry Potter', 'Argus Filch in Harry Potter', 'Amycus Carrow in Harry Potter', 'Bill Weasley in Harry Potter', 'Luna Lovegood in Harry Potter', 'Barty Crouch Sr in Harry Potter', 'Vernon Dursley in Harry Potter', 'Pansy Parkinson in Harry Potter', 'Aurora Sinistra in Harry Potter', 'Barty Crouch Jr in Harry Potter', 'Scabbers in Harry Potter', 'Tom Riddle in Harry Potter', 'Pius Thicknesse in Harry Potter', 'Buckbeak in Harry Potter', 'George Weasley in Harry Potter', 'Ollivander in Harry Potter', 'Wilhelmina Grubbly-Plank in Harry Potter', 'Rita Skeeter in Harry Potter', 'Lily Evans in Harry Potter', 'Arabella Figg in Harry Potter', 'Lavender Brown in Harry Potter', 'Lee Jordan in Harry Potter', 'Stan Shunpike in Harry Potter', 'Aberforth Dumbledore in Harry Potter', 'Augusta Longbottom in Harry Potter', 'Albus Dumbledore in Harry Potter', 'Nearly Headless Nick in Harry Potter', 'Quirinus Quirrell in Harry Potter', 'Thorfinn Rowle in Harry Potter', 'Antonin Dolohov in Harry Potter', 'Sybill Trelawney in Harry Potter', 'Albert Runcorn in Harry Potter', 'Severus Snape in Harry Potter', 'Mundungus Fletcher in Harry Potter', 'Kingsley Shacklebolt in Harry Potter', 'Rubeus Hagrid in Harry Potter', 'Crookshanks in Harry Potter', 'Marietta Edgecombe in Harry Potter', 'The Fat Friar in Harry Potter', 'Ludo Bagman in Harry Potter', 'Frank Longbottom in Harry Potter', 'Igor Karkaroff in Harry Potter', 'Narcissa Malfoy in Harry Potter', 'Bathilda Bagshot in Harry Potter', 'Gellert Grindelwald in Harry Potter', 'Porpentina Goldstein in Harry Potter', 'Silvanus Kettleburn in Harry Potter', 'Justin Finch-Fletchley in Harry Potter', 'Irma Pince in Harry Potter', 'Oliver Wood in Harry Potter', 'Mafalda Hopkirk in Harry Potter', 'Seamus Finnigan in Harry Potter', 'Dobby in Harry Potter', 'Fred Weasley in Harry Potter', 'Nagini in Harry Potter', 'James Potter in Harry Potter', 'Cornelius Fudge in Harry Potter', 'Rolanda Hooch in Harry Potter', 'Alastor Moody in Harry Potter', 'Rufus Scrimgeour in Harry Potter', 'Remus Lupin in Harry Potter', 'Cedric Diggory in Harry Potter', 'Gregory Goyle in Harry Potter', 'Arthur Weasley in Harry Potter', 'Amelia Bones in Harry Potter', 'Myrtle Warren in Harry Potter', 'Lucius Malfoy in Harry Potter', 'Cho Chang in Harry Potter', 'Poppy Pomfrey in Harry Potter', 'Marge Dursley in Harry Potter', 'Minerva Mcgonagall in Harry Potter', 'Nymphadora Tonks in Harry Potter', 'Molly Weasley in Harry Potter', 'Fleur Delacour in Harry Potter', 'Morfin Gaunt in Harry Potter', 'Frank Bryce in Harry Potter', 'Elphias Doge in Harry Potter', 'Ron Weasley in Harry Potter', 'Zacharias Smith in Harry Potter', 'Alicia Spinnet in Harry Potter', 'Phineas Nigellus Black in Harry Potter', 'Dolores Jane Umbridge in Harry Potter', 'The Bloody Baron in Harry Potter', 'Walden Macnair in Harry Potter', 'Horace Slughorn in Harry Potter', 'Viktor Krum in Harry Potter', 'Firenze in Harry Potter', 'Harry Potter in Harry Potter', 'Augustus Rookwood in Harry Potter', 'Pomona Sprout in Harry Potter', 'Gilderoy Lockhart in Harry Potter', 'Percy Weasley in Harry Potter', 'Fawkes in Harry Potter', 'Filius Flitwick in Harry Potter', 'Bellatrix Lestrange in Harry Potter', 'Hedwig in Harry Potter', 'Dudley Dursley in Harry Potter', 'Grawp in Harry Potter', 'Neville Longbottom in Harry Potter', 'Parvati Patil in Harry Potter', 'Hannah Abbott in Harry Potter', 'Sirius Black in Harry Potter', 'Dedalus Diggle in Harry Potter', 'Charlie Weasley in Harry Potter', 'Olympe Maxime in Harry Potter', 'Draco Malfoy in Harry Potter', 'Antioch Peverell in Harry Potter', 'Regulus Black in Harry Potter', 'Petunia Dursley in Harry Potter', 'The Waif in Game Of Thrones', 'Eddard Stark in Game Of Thrones', 'Petyr Baelish in Game Of Thrones', 'Tywin Lannister in Game Of Thrones', 'Joffrey Baratheon in Game Of Thrones', 'Euron Greyjoy in Game Of Thrones', 'Rhaegar Targaryen in Game Of Thrones', 'Renly Baratheon in Game Of Thrones', 'Qyburn in Game Of Thrones', 'Tormund in Game Of Thrones', 'Lord Varys in Game Of Thrones', 'Jon Snow in Game Of Thrones', 'Olenna Tyrell in Game Of Thrones', 'Catelyn Stark in Game Of Thrones', 'Jaime Lannister in Game Of Thrones', 'Alliser Thorne in Game Of Thrones', 'Tormund Giantsbane in Game Of Thrones', 'Maester Luwin in Game Of Thrones', 'Meryn Trant in Game Of Thrones', 'Bran Stark in Game Of Thrones', 'Shae in Game Of Thrones', 'Bronn in Game Of Thrones', 'Lancel Lannister in Game Of Thrones', 'Janos Slynt in Game Of Thrones', 'Ellaria Sand in Game Of Thrones', 'Hodor in Game Of Thrones', 'Tyrion Lannister in Game Of Thrones', 'Kevan Lannister in Game Of Thrones', 'Edmure Tully in Game Of Thrones', 'Samwell Tarly in Game Of Thrones', 'Stannis Baratheon in Game Of Thrones', 'Robb Stark in Game Of Thrones', 'Viserys Targaryen in Game Of Thrones', 'Tommen Baratheon in Game Of Thrones', 'Lyanna Mormont in Game Of Thrones', 'Daenerys Targaryen in Game Of Thrones', 'Cersei Lannister in Game Of Thrones', 'Rast in Game Of Thrones', 'Lyanna Stark in Game Of Thrones', 'Barristan Selmy in Game Of Thrones', 'Davos Seaworth in Game Of Thrones', 'Margaery Tyrell in Game Of Thrones', 'Gendry in Game Of Thrones', 'Maester Aemon in Game Of Thrones', 'Arya Stark in Game Of Thrones', 'Theon Greyjoy in Game Of Thrones', 'Sansa Stark in Game Of Thrones', 'Yara Greyjoy in Game Of Thrones', 'Roose Bolton in Game Of Thrones', 'Sandor Clegane in Game Of Thrones', 'Loras Tyrell in Game Of Thrones', 'Ramsay Bolton in Game Of Thrones', 'Brienne Of Tarth in Game Of Thrones', 'Melisandre in Game Of Thrones', 'Jorah Mormont in Game Of Thrones', 'Myrcella Baratheon in Game Of Thrones', 'Robert Baratheon in Game Of Thrones', 'Iron Man in Marvel Cinematic Universe', 'Karen Page in Marvel Cinematic Universe', 'Thaddeus Ross in Marvel Cinematic Universe', 'Groot in Marvel Cinematic Universe', 'Ultron in Marvel Cinematic Universe', 'Obadiah Stane in Marvel Cinematic Universe', 'Loki in Marvel Cinematic Universe', 'Black Widow in Marvel Cinematic Universe', 'Ned Leeds in Marvel Cinematic Universe', 'Valkyrie in Marvel Cinematic Universe', 'Black Panther in Marvel Cinematic Universe', 'Daredevil in Marvel Cinematic Universe', 'Nick Fury in Marvel Cinematic Universe', 'Vision in Marvel Cinematic Universe', 'Hela in Marvel Cinematic Universe', 'Liz Toomes in Marvel Cinematic Universe', 'Howard Stark in Marvel Cinematic Universe', 'Arnim Zola in Marvel Cinematic Universe', 'Spider-Man in Marvel Cinematic Universe', 'Nebula in Marvel Cinematic Universe', 'Pepper Potts in Marvel Cinematic Universe', 'Malekith in Marvel Cinematic Universe', 'Hawkeye in Marvel Cinematic Universe', 'Scarlet Witch in Marvel Cinematic Universe', 'The Other in Marvel Cinematic Universe', 'Hulk in Marvel Cinematic Universe', 'Yondu Udonta in Marvel Cinematic Universe', 'Thanos in Marvel Cinematic Universe', 'Phil Coulson in Marvel Cinematic Universe', 'Falcon in Marvel Cinematic Universe', 'Hank Pym in Marvel Cinematic Universe', 'Maria Hill in Marvel Cinematic Universe', 'Punisher in Marvel Cinematic Universe', 'Jarvis in Marvel Cinematic Universe', 'Peggy Carter in Marvel Cinematic Universe', 'Sif in Marvel Cinematic Universe', 'Quicksilver in Marvel Cinematic Universe', 'Ulysses Klaue in Marvel Cinematic Universe', 'Collector in Marvel Cinematic Universe', 'Carol Danvers in Marvel Cinematic Universe', 'Kingpin in Marvel Cinematic Universe', 'Alexander Pierce in Marvel Cinematic Universe', 'Red Skull in Marvel Cinematic Universe', 'Foggy Nelson in Marvel Cinematic Universe', 'Heimdall in Marvel Cinematic Universe', 'War Machine in Marvel Cinematic Universe', 'Odin in Marvel Cinematic Universe', 'Captain America in Marvel Cinematic Universe', 'Star-Lord in Marvel Cinematic Universe', 'Wasp in Marvel Cinematic Universe', 'Ant-Man in Marvel Cinematic Universe', 'Doctor Strange in Marvel Cinematic Universe', 'Thor in Marvel Cinematic Universe', 'Gamora in Marvel Cinematic Universe', 'Sharon Carter in Marvel Cinematic Universe', 'Drax The Destroyer in Marvel Cinematic Universe', 'Rocket Raccoon in Marvel Cinematic Universe', 'Happy Hogan in Marvel Cinematic Universe', 'Jane Foster in Marvel Cinematic Universe', 'Bucky Barnes in Marvel Cinematic Universe', 'Mace Windu in Star Wars', 'Chewbacca in Star Wars', 'Orson Krennic in Star Wars', 'Darth Vader in Star Wars', "Qi'Ra in Star Wars", 'Yoda in Star Wars', 'Qui-Gon Jinn in Star Wars', 'Cassian Andor in Star Wars', 'Asajj Ventress in Star Wars', 'Wedge Antilles in Star Wars', 'Kylo Ren in Star Wars', 'Lando Calrissian in Star Wars', 'Finn in Star Wars', 'Poe Dameron in Star Wars', 'Grand Admiral Thrawn in Star Wars', 'Captain Phasma in Star Wars', 'Padmé Amidala in Star Wars', 'Rose Tico in Star Wars', 'Grand Moff Tarkin in Star Wars', 'Saw Gerrera in Star Wars', 'Jyn Erso in Star Wars', 'Palpatine in Star Wars', 'Admiral Piett in Star Wars', 'Luke Skywalker in Star Wars', 'Nien Nunb in Star Wars', 'Ahsoka Tano in Star Wars', 'Princess Leia in Star Wars', 'Iden Versio in Star Wars', 'C-3Po in Star Wars', 'Bail Organa in Star Wars', 'R2-D2 in Star Wars', 'Rey in Star Wars', 'General Hux in Star Wars', 'Obi-Wan Kenobi in Star Wars', 'Darth Maul in Star Wars', 'Han Solo in Star Wars', 'Jango Fett in Star Wars', 'Richard Reiben in Saving Private Ryan', 'David in Star Trek: The Wrath Of Khan', 'Senator Kelly in X-Men', 'Superman in Superman Iii', 'Sal in Do The Right Thing', 'Aunt May (Rosemary Harris) in Spider-Man', 'Steve Stifler in American Pie', 'Cecile Caldwell in Cruel Intentions', 'Richard Gecko in From Dusk Till Dawn', 'Cameron James in 10 Things I Hate About You', 'Professor in The Bourne Identity', 'Ellen Brody in Jaws', 'Dr. Doom (Story Series) in Fantastic Four', 'Professor Barnhardt in The Day The Earth Stood Still', 'Quint in Jaws', 'Henry Hill in Goodfellas', 'Dr. Lazarus in Galaxy Quest', 'Floyd Family in 2001: A Space Odyssey', 'Sick Boy in Trainspotting', 'Paulie Pennino in Rocky', 'William Wallace in Braveheart', 'Ellie Sattler in Jurassic Park', 'Ricardo "Rico" Tubbs in Miami Vice', 'Helen Tasker in True Lies', 'Lucius in Planet Of The Apes', 'Padishah Emperor in Dune', 'Ned Rubenstein in Friday The 13Th', 'Jonathan Carnahan in The Mummy', 'Evelyn Stockard-Price in House On Haunted Hill', 'Julia Cotton in Hellraiser', 'John Fujima in Miami Vice', 'John H. Miller in Saving Private Ryan', 'Steven Meeks in Dead Poets Society', 'Jerome Eugene Morrow in Gattaca', 'Larry Cotton in Hellraiser', 'Nauls in The Thing', 'Patrick Verona in 10 Things I Hate About You', 'Jessica Rabbit in Who Framed Roger Rabbit', 'The Wizard Of Oz (Person) in The Wizard Of Oz', 'John Keating in Dead Poets Society', 'Leon Kowalski in Blade Runner', 'Kay Adams in The Godfather', 'Vampira in Ed Wood', 'Adrian in Little Nicky', 'Jade in Do The Right Thing', 'Sheriff Burke in Scream', 'Carla Brody in Jaws', 'Kruge in Star Trek Iii: The Search For Spock', "Buggin' Out in Do The Right Thing", 'Tin Man in The Wizard Of Oz', 'Jamie Sullivan in A Walk To Remember', 'Gina Calabrese in Miami Vice', 'Al Powell in Die Hard', 'Randy Meeks in Scream', 'Vanessa Loring in Juno', 'Todd Anderson in Dead Poets Society', 'Seth Gecko in From Dusk Till Dawn', 'John Williams in Blue Velvet', 'Gillian Taylor in Star Trek Iv: The Voyage Home', 'Otis in Superman', 'Mr. Blonde in Reservoir Dogs', 'Michael Corleone in The Godfather', 'Glen Lantz in A Nightmare On Elm Street', 'Barbara Wellesley in Blow', 'Tania Johnson in Rush Hour', 'Lewis Mason in The Rock', 'Will Bloom in Big Fish', 'Pamela Landy in The Bourne Supremacy', 'Vox in The Time Machine', 'Solon Han in Rush Hour', 'Egon Spengler in Ghostbusters Ii', 'Marla Singer in Fight Club', 'Heather Duke in Heathers', 'Eddie Valiant in Who Framed Roger Rabbit', 'Paul Finch in American Pie', 'Hannibal Lecter in The Silence Of The Lambs', 'Tyler Durden in Fight Club', 'Rachael in Blade Runner', 'Donald W. Blackburn in House On Haunted Hill', 'Renton in Trainspotting', 'Kyle Reese in The Terminator', 'Leon Henderson in Lon', 'Holly Gennero in Die Hard', 'Cyclops in X-Men', 'Lou in Fight Club', 'Klaatu in The Day The Earth Stood Still', 'Jessica Atreides in Dune', 'Argyle in Die Hard', 'Heather in American Pie', 'John Sullivan in Frequency', 'Neo in The Matrix', 'Roc Ingersol in Galaxy Quest', 'Shinzon in Star Trek: Nemesis','Satch Deleon in Frequency', 'King Edward Longshanks in Braveheart', 'R.J. Macready in The Thing', 'Detective Holdaway in Reservoir Dogs', 'Eddie Baker in House On Haunted Hill', 'Pris in Blade Runner', 'Baby Herman in Who Framed Roger Rabbit', 'Roger Rabbit in Who Framed Roger Rabbit', 'Kirsty Cotton in Hellraiser', 'Marcie Stanler in Friday The 13Th', 'Stu Macher in Scream', 'Anton Chigurh in No Country For Old Men', 'Suzie Toller in Wild Things', 'Roy Batty in Blade Runner', 'Martia in Star Trek Vi: The Undiscovered Country', 'Sweet Dick Willie in Do The Right Thing', 'Tina in Do The Right Thing', 'Clay in Hellboy', 'Suran in Star Trek: Nemesis', 'George Taylor in Planet Of The Apes', 'Neil Perry in Dead Poets Society', 'Beni Gabor in The Mummy', 'Milkman Jerry in Fargo', 'Bud Fox in Wall Street', 'Skull Cowboy in The Crow', 'Annie Wilkes in Misery', 'Rose Dewitt Bukater in Titanic', 'Cowardly Lion in The Wizard Of Oz', 'The President in Planet Of The Apes', 'David Bowman in 2001: A Space Odyssey', "Steve O'Donnell in Hellraiser", 'Sally in The Nightmare Before Christmas', 'Frank Poole in 2001: A Space Odyssey', 'Murphy Macmanus in The Boondock Saints', 'Edgar Frog in The Lost Boys', 'Ram Sweeney in Heathers', 'Dan Dreiberg in Watchmen', 'Stilgar in Dune', 'Worf in Star Trek: Nemesis', 'Barrel in The Nightmare Before Christmas', 'Brenda Meeks in Scary Movie 2','Ruby in Star Trek: First Contact', 'Ann Darrow in King Kong', 'Matt Hooper in Jaws', 'Ed Traxler in The Terminator', 'Walter Stevens in Miami Vice', 'Larry Vaughn in Jaws', 'Helen Benson in The Day The Earth Stood Still', 'Thomas Andrews in Titanic', 'Pino in Do The Right Thing', 'Anderson in Saving Private Ryan', 'Glinda in The Wizard Of Oz', 'Virgil Sollozzo in The Godfather', 'Brenda Jones in Friday The 13Th', 'Steve in Friday The 13Th', 'Invisible Boy in Mystery Men', 'Caledon Hockley in Titanic', 'Rick Blaine in Casablanca', 'Andrei Smyslov in 2001: A Space Odyssey', 'Jon Osterman in Watchmen', 'Martha And Jonathan Kent in Superman', 'Paul Smecker in The Boondock Saints', 'Gallatin in Star Trek: Insurrection', 'Ben Grimm (Story Series) in Fantastic Four', 'Watson Pritchett in House On Haunted Hill', 'Garry in The Thing', 'Laurie in Halloween', 'Little Nicky in Little Nicky', 'Gale Nolan in Dead Poets Society', 'Maude Lebowski in The Big Lebowski', 'Colonel James Doolittle in Pearl Harbor', 'Steven H. Price in House On Haunted Hill', 'Detective Greenly in The Boondock Saints', 'Gurney Halleck in Dune', 'Sarah Connor in The Terminator', 'J. Jonah Jameson (J.K. Simmons) in Spider-Man', 'Hamm in Toy Story', 'Ml in Do The Right Thing', 'Frank Booth in Blue Velvet', 'Lois Lane in Superman Iii', 'Cypher in The Matrix', 'Ichabod Crane in Sleepy Hollow', 'Jack Thayer in Titanic', 'Walter Kovacs in Watchmen', 'Honorius in Planet Of The Apes', 'Mr. White in Reservoir Dogs', 'Harry Ellis in Die Hard', 'Miles Jergens in Rocky', 'Morpheus in The Matrix', 'Harry Osborn (James Franco) in Spider-Man', 'Marcus Aurelius in Gladiator', 'Juno Skinner in True Lies', 'Antonius Proximo in Gladiator', 'Tommy in Trainspotting', 'Laurie Juspeczyk in Watchmen','Laurie Juspeczyk in Watchmen'];

var countries2 = ['John Hammond in Jurassic Park', 'Norris in The Thing', 'Nichols in Star Trek Iv: The Voyage Home', 'Commodus in Gladiator', 'Rod Lane in A Nightmare On Elm Street', 'Eric Draven in The Crow', 'Jean Grey in X-Men', 'Childs in The Thing', 'Mr. Potato Head in Toy Story', 'Robert Neville in I Am Legend', 'Jack Shepard in Frequency', 'Julia Sullivan in Frequency', 'Iran Deckard in Blade Runner', 'Donny in The Big Lebowski', 'George Whitman in Hellboy', 'Vicki Vale in Batman', 'Dorothy Vallens in Blue Velvet', 'John Harriman in Star Trek: Generations', 'Hal Vukovich in The Terminator', 'Annette Hargrove in Cruel Intentions', 'Daniel Jackson in Saving Private Ryan', 'Woody in Toy Story', 'Paul Atreides in Dune', 'Andy in Toy Story', 'Ruth Elizabeth Becker in Titanic', 'Lucilla in Gladiator', 'John Arnold in Jurassic Park', 'Alice Hardy in Friday The 13Th', 'Burt Gummer in Tremors', 'Adrian Balboa in Rocky', 'Gale Riley in Scream', 'Gordo in Frequency', 'Sonny Corleone in The Godfather', 'Guinan in Star Trek: Generations', 'Buzz Lightyear in Toy Story', 'Data in Star Trek: Generations', 'Deanna Troi in Star Trek: Nemesis', 'Mother Sister in Do The Right Thing', 'Dorothy Gale in The Wizard Of Oz', 'Jack Nicholson in Batman', 'Dave Holden in Blade Runner', 'Sybok in Star Trek V: The Final Frontier', 'Signora Clemenza in The Godfather', 'Tony Gazzo in Rocky', 'Nancy Thompson in A Nightmare On Elm Street', 'Anij in Star Trek: Insurrection', 'James "Sonny" Crockett in Miami Vice', 'Agatha in Minority Report', 'Kat Stratford in 10 Things I Hate About You', 'Ray Wilkins in Scary Movie 2', 'Uncle Ben (Cliff Robertson) in Spider-Man', 'Slinky in Toy Story', 'Hal 9000 in 2001: A Space Odyssey', 'Eldon Tyrell in Blade Runner', 'Connor Macmanus in The Boondock Saints', 'Rex in Toy Story', 'Tolian Soran in Star Trek: Generations', 'Peter Silberman in The Terminator', 'Kate Fuller in From Dusk Till Dawn', 'Matthew Dougherty in Star Trek: Insurrection', 'Emmett Richmond in Legally Blonde', 'Jacob Fuller in From Dusk Till Dawn', 'Scotty in Star Trek: Generations', 'Ian Malcolm in Jurassic Park', 'The Man With All The Marbles in Fargo', 'Tina Gray in A Nightmare On Elm Street', 'The Joker in Batman', 'Wally in Minority Report', 'Frank Cotton in Hellraiser', 'J.T. Esteban in Star Trek Iii: The Search For Spock', 'Sid Phillips in Toy Story', 'Heather Chandler in Heathers', 'Clarice Starling in The Silence Of The Lambs', 'Mrs. Potato Head in Toy Story', 'Grange in The Crow', 'Rhonda Lebeck in Tremors', 'Isabella in Miami Vice', 'Ward Abbott in The Bourne Supremacy', 'Brandt in The Big Lebowski', 'Cassius in Little Nicky', 'Peter Venkman in Ghostbusters Ii', 'Emma in The Time Machine', 'Spider-Man (Tobey Maguire) in Spider-Man', 'Marge Thompson in A Nightmare On Elm Street', 'Alan Frog in The Lost Boys', 'Detective Hugo in Gattaca', 'Walter Stratford in 10 Things I Hate About You', 'Dewey Riley in Scream', 'Begbie in Trainspotting', 'Carl Denham in King Kong', 'Kurt Kelly in Heathers', 'Blade Bummer in Blade', 'Saavik in Star Trek Iii: The Search For Spock', 'Reed Richards (Story Series) in Fantastic Four', 'Kelly Van Ryan in Wild Things', 'Sergeant Albrecht in The Crow', 'Vito in Do The Right Thing', 'Edward in Big Fish', 'Earl Bassett in Tremors', 'Chris Noel in Dead Poets Society', 'Mara in The Time Machine', 'Donald Gennaro in Jurassic Park', 'Nyota Uhura in Star Trek Vi: The Undiscovered Country', 'Monica in Mystery Men', 'Lex Luthor in Superman', 'Alexander Knox in Batman', 'Professor X in X-Men', 'Landon Carter in A Walk To Remember', 'Borg Queen in Star Trek: First Contact', 'Mickey Goldmill in Rocky', 'Martin "Marty" Castillo in Miami Vice', 'Mara Leonin in Highlander', 'Beverly Crusher in Star Trek: First Contact', 'The Oracle in The Matrix', 'Lieutenant Starck in Event Horizon', 'Magneto in X-Men', 'John Myers in Hellboy', 'Harry Bryant in Blade Runner', 'Kevin Myers in American Pie', 'Heather Mcnamara in Heathers', 'Frank Sullivan in Frequency', 'Will Decker in Star Trek: The Motion Picture', 'Apollo Creed in Rocky', 'Clear Rivers in Final Destination', 'Juno in Juno', 'James Carter in Rush Hour', 'Sandy Williams in Blue Velvet', 'Batman in Batman', 'James_T._Kirk in Star Trek: The Wrath Of Khan', 'Hans Gruber in Die Hard', 'Casanova Frankenstein in Mystery Men', 'Paul Sheldon in Misery', 'Jennifer Hill in Big Fish', 'Timothy E. Upham in Saving Private Ryan', 'José Yero in Miami Vice', 'Gordon Gekko in Wall Street', 'Doctor Miguelito Loveless in Wild Wild West', 'Irwin Wade in Saving Private Ryan', 'Mr. Orange in Reservoir Dogs', 'Diane in Trainspotting', 'Agent Smith in The Matrix', 'Gerard Pitts in Dead Poets Society', 'Radio Raheem in Do The Right Thing', 'Capt. Rafe Mccawley in Pearl Harbor', 'Sidney Prescott in Scream', 'Trinity in The Matrix', 'Human Torch (Story Series) in Fantastic Four', 'Wolverine in X-Men', 'Michelle Flaherty in American Pie', 'Joachim in Star Trek: The Wrath Of Khan', 'Alexander Conklin in The Bourne Supremacy', 'The Wicked Witch Of The West in The Wizard Of Oz', 'Lieutenant Peters in Event Horizon', 'Robert Muldoon in Jurassic Park', 'Katrina Van Tassel in Sleepy Hollow', 'Irene Cassini in Gattaca', 'Reverend Mother in Dune', 'Paulette Bonafonté in Legally Blonde', 'Bianca Stratford in 10 Things I Hate About You', 'Da Mayor in Do The Right Thing', 'Knox Overstreet in Dead Poets Society', 'Brooke Taylor-Windham in Legally Blonde', 'Geordi La Forge in Star Trek: First Contact', 'Sara Wolfe in House On Haunted Hill', 'Jeffrey Beaumont in Blue Velvet', 'David Della Rocco in The Boondock Saints', 'Alexander Hartdegen in The Time Machine', 'Adrian Veidt in Watchmen', 'Curator in The Mummy', 'Elle Woods in Legally Blonde', 'J.F. Sebastian in Blade Runner', 'Alan Grant in Jurassic Park', 'Detective Duffy in The Boondock Saints', 'Ilia in Star Trek: The Motion Picture', 'Faust in Alien', 'Evelyn Johnson in Pearl Harbor', 'Jor-El in Superman', 'Blair in The Thing', 'Nadia in American Pie', 'Veronica Sawyer in Heathers', 'Spud in Trainspotting', 'Warner Huntington Iii in Legally Blonde', 'Walter Sobchak in The Big Lebowski', 'Terrell in Star Trek: The Wrath Of Khan', 'Frank Moran in Highlander', 'Bela Lugosi in Ed Wood', 'Bruce Timm in Batman', 'Sarek in Star Trek Iii: The Search For Spock', 'Bobby in The Day The Earth Stood Still', 'John Landon in Planet Of The Apes', 'Copper in The Thing', 'Charlie Dalton in Dead Poets Society', 'Hunter Borgia in Alien', 'Gideon in Minority Report', 'Lamar Burgess in Minority Report', 'Tatum Riley in Scream', 'Bill Brown in Friday The 13Th', 'Billy Loomis in Scream', 'Capt. Danny Walker in Pearl Harbor', 'Casey Becker in Scream', 'Mr. Pink in Reservoir Dogs', 'Swanney in Trainspotting', 'Eve Teschmacher in Superman', 'Marie in Rocky', 'The Dude in The Big Lebowski', 'Kathryn Merteuil in Cruel Intentions', 'Jason Bourne in The Bourne Supremacy', 'Mookie in Do The Right Thing', 'Harry Tasker in True Lies', 'Yan Naing Lee in Rush Hour', 'Catwoman in Catwoman', 'Invisible Woman (Story Series) in Fantastic Four', 'Nicky Parsons in The Bourne Supremacy', 'Warren Russ in Rush Hour', 'Sulu in Star Trek: The Motion Picture', 'Spock in Star Trek: The Wrath Of Khan', 'Palmer in The Thing', 'Guiseppe Yakavetta in The Boondock Saints', 'Artim in Star Trek: Insurrection', "Evelyn O'Connell in The Mummy", 'Chekov in Star Trek Iv: The Voyage Home', 'Maximus Decimus Meridius in Gladiator'];

var countries = countries1.concat(countries2);

$('#submit-btn').click(function () {

	document.data = returnDict;
	var catchphrace = $('#catchphrase').val();
	var adj = $('#adjectives').val();

	var character = $('#charactername').val();
	if (!countries.includes(character)){
		var character= "";
	}
	else{
		var character= character.split(' in ')[0].split(' ').join('_');
	}
	if (document.getElementById('hpchecked').checked) {
            var hp="yes";
        } else {
            var hp="no";
        }
 	if (document.getElementById('gotchecked').checked) {
            var got="yes";
        } else {
            var got="no";
        }
 	if (document.getElementById('marvelchecked').checked) {
            var mar="yes";
        } else {
            var mar="no";
        }
    if (document.getElementById('swchecked').checked) {
            var sw="yes";
        } else {
            var sw="no";
        }
    if (document.getElementById('otherchecked').checked) {
            var other="yes";
        } else {
            var other="no";
        }



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
			"&character=" +character +
			"&hp=" + hp +
			"&got=" + got +
			"&mar=" + mar +
			"&sw=" + sw +
			"&other=" + other
			;
	document.location.href = url;


});

// Refresh the screen to show a new quiz if they click the retake quiz button
$('#retake-btn').click(function () {
	document.location.href = "/";
});

$('#home-btn').click(function () {
	document.location.href = "/";
});

