function openCity(evt, cityName) {
    console.log("here");
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

var data = [];
var token = "";

jQuery(document).ready(function() {
    var slider = $("#max_words");
    slider.on("change mousemove", function(evt) {
        console.log(slider.val());
        $("#label_max_words").text("# words in summary: " + slider.val());
    });

    var slider2 = $("#max_summaries");
    slider2.on("change mousemove", function(evt) {
        $("#Number_of_summaries").text("# of summaries: " + slider2.val());
        console.log(slider2.val());
    });
    $("#Number_of_summaries").text("# of summaries: " + slider2.val());

    $("#btn-process").on("click", function() {
        input_text = $("#txt_input").val();
        model = $("#input_model").val();
        num_words = $("#max_words").val();
        num_beams = $("#num_beams").val();
        $.ajax({
                url: "/predict",
                type: "post",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify({
                    input_text: input_text,
                    model: model,
                    num_words: num_words,
                    num_beams: num_beams,
                }),
                beforeSend: function() {
                    $(".overlay").show();
                },
                complete: function() {
                    $(".overlay").hide();
                },
            })
            .done(function(jsondata, textStatus, jqXHR) {
                console.log(jsondata);
                $("#input_summary").val(jsondata["response"]["summary"]);
            })
            .fail(function(jsondata, textStatus, jqXHR) {
                alert(jsondata["responseJSON"]["message"]);
            });
    });
});

/*--------------------------------copy functions--------------------------------------*/

function copyFunction1() {
    /* Get the text field */
    var copyText = document.getElementById("summary1");
    console.log("mm");

    let elementText = copyText.textContent; //get the text content from the element
    navigator.clipboard.writeText(elementText);
    /* Select the text field */
}

function copyFunction2() {
    /* Get the text field */
    var copyText = document.getElementById("summary2");
    console.log("mm");

    let elementText = copyText.textContent; //get the text content from the element
    navigator.clipboard.writeText(elementText);
    /* Select the text field */
}

function copyFunction3() {
    /* Get the text field */
    var copyText = document.getElementById("summary3");
    console.log("mm");

    let elementText = copyText.textContent; //get the text content from the element
    navigator.clipboard.writeText(elementText);
    /* Select the text field */
}

function copyFunction4() {
    /* Get the text field */
    var copyText = document.getElementById("summary4");
    console.log("mm");

    let elementText = copyText.textContent; //get the text content from the element
    navigator.clipboard.writeText(elementText);
    /* Select the text field */
}

/*---------------------------------side bar elements-------------------------------------------*/

function showDivSummaries() {
    console.log("as");
    //document.getElementsByClassName("home-section2").style.display = "block";
    var cols = document.getElementsByClassName("home-section2");
    for (i = 0; i < cols.length; i++) {
        cols[i].style.display = "block";
    }

    var cols = document.getElementsByClassName("home-section3");
    for (i = 0; i < cols.length; i++) {
        cols[i].style.display = "none";
    }
}

function showDivSummaries2() {
    console.log("as");
    //document.getElementsByClassName("home-section2").style.display = "block";

    var cols = document.getElementsByClassName("home-section3");
    for (i = 0; i < cols.length; i++) {
        cols[i].style.display = "block";
    }
    var cols = document.getElementsByClassName("home-section2");
    for (i = 0; i < cols.length; i++) {
        cols[i].style.display = "none";
    }
}

/*-----------------------------------------popupwindow----------------------------- */
$(document).ready(function() {
    $(window).load(function() {
        $(".trigger_popup_fricc1").click(function() {
            $(".hover_bkgr_fricc1").show();
            $(".hover_bkgr_fricc2").hide();
            $(".hover_bkgr_fricc3").hide();
        });

        $(".hover_bkgr_fricc1").click(function() {
            $(".hover_bkgr_fricc1").hide();
        });

        $(".popupCloseButton1").click(function() {
            $(".popup_content1").hide();
            console.log("banddd");
        });

        $(".trigger_popup_fricc2").click(function() {
            $(".hover_bkgr_fricc2").show();
            $(".hover_bkgr_fricc1").hide();
            $(".hover_bkgr_fricc3").hide();
        });
        $(".hover_bkgr_fricc2").click(function() {
            $(".hover_bkgr_fricc2").hide();
        });
        $(".popupCloseButton2").click(function() {
            $(".popup_content2").hide();
            console.log("banddd");
        });

        $(".trigger_popup_fricc3").click(function() {
            $(".hover_bkgr_fricc3").show();
            $(".hover_bkgr_fricc2").hide();
            $(".hover_bkgr_fricc1").hide();
        });
        $(".hover_bkgr_fricc3").click(function() {
            $(".hover_bkgr_fricc3").hide();
        });
        $(".popupCloseButton3").click(function() {
            $(".popup_content3").hide();
            console.log("banddd");
        });
    });

    /////////////////audio
    $("#listen-summary1").click(function() {
        // Attach this function to all mouseenter events for 'a' tags
        responsiveVoice.cancel(); // Cancel anything else that may currently be speaking
        var text1 = $("#summary1").text();
        responsiveVoice.speak(text1);
        // Speak the text contents of all nodes within the current 'a' tag
        console.log("....here");
    });
    $("#pause-summary1").click(function() {
        responsiveVoice.pause();
    });
    $("#resume-summary1").click(function() {
        responsiveVoice.resume();
    });

    $("#listen-summary2").click(function() {
        // Attach this function to all mouseenter events for 'a' tags
        responsiveVoice.cancel(); // Cancel anything else that may currently be speaking
        var text1 = $("#summary2").text();
        responsiveVoice.speak(text1); // Speak the text contents of all nodes within the current 'a' tag
    });
    $("#pause-summary2").click(function() {
        responsiveVoice.pause();
    });
    $("#resume-summary2").click(function() {
        responsiveVoice.resume();
    });

    $("#listen-summary3").click(function() {
        // Attach this function to all mouseenter events for 'a' tags
        responsiveVoice.cancel(); // Cancel anything else that may currently be speaking
        var text1 = $("#summary3").text();
        responsiveVoice.speak(text1); // Speak the text contents of all nodes within the current 'a' tag
    });
    $("#pause-summary3").click(function() {
        responsiveVoice.pause();
    });
    $("#resume-summary3").click(function() {
        responsiveVoice.resume();
    });

    $("#listen-summary4").click(function() {
        // Attach this function to all mouseenter events for 'a' tags
        responsiveVoice.cancel(); // Cancel anything else that may currently be speaking
        var text1 = $("#summary4").text();
        responsiveVoice.speak(text1); // Speak the text contents of all nodes within the current 'a' tag
    });
    $("#pause-summary4").click(function() {
        responsiveVoice.pause();
    });
    $("#resume-summary4").click(function() {
        responsiveVoice.resume();
    });

    $("#listen-summary5").click(function() {
        // Attach this function to all mouseenter events for 'a' tags
        responsiveVoice.cancel(); // Cancel anything else that may currently be speaking
        var text1 = $("#summary5").text();
        responsiveVoice.speak(text1); // Speak the text contents of all nodes within the current 'a' tag
    });
    $("#pause-summary5").click(function() {
        responsiveVoice.pause();
    });
    $("#resume-summary5").click(function() {
        responsiveVoice.resume();
    });

    /////////////////////////////////////////loader



});