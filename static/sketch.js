let canvas, pg, colorPicker, eraser, reset;
let mode = 0;
let drawing = 0;
let currentTag = '';
let div = document.getElementById("canvas-p5-container");
let brushSize = $("input[name='brush-size']:checked").val();

function setup() {
  let width = div.offsetWidth * 0.95;
  let height = width * 0.75;
  width = Math.round(width);
  height = Math.round(height);
  canvas = createCanvas(width, height);
  
  pg = createGraphics(width, height);

  $("input[name='brush-size']").change(function() {
    brushSize = $("input[name='brush-size']:checked").val();
  });

  pg.background('#ffffff');
  canvas.parent('canvas-p5-container');
  canvas.addClass('drawing-canvas');
  
  colorPicker = createColorPicker('#000000');
  colorPicker.parent('panel-p5-container');
  colorPicker.addClass('drawing-button');
  colorPicker.style('background-color', 'white')
    
  eraser = createButton();
  eraser.mouseClicked(switchEraser);
  eraser.parent('panel-p5-container');
  eraser.addClass('drawing-button');
  eraser.addClass('drawing-button-eraser');
  $(eraser.elt).html('<i class="fa fa-solid fa-eraser"></i>');

  reset = createButton();
  reset.mouseClicked(resetCanvas);
  reset.parent('panel-p5-container');
  reset.addClass('drawing-button');
  reset.addClass('drawing-button-reset');
  $(reset.elt).html('<i class="fa fa-solid fa-trash"></i>');
  reset.style('background-color', '#0c9b7e')

  loadImage('/static/notallowed.png', img => {
    pg.image(img, 0, 0, width, height);
    noLoop();
    mode = -1;
  })
}

  function importTags() {
    $('#stacked-drawing-tags').inputTags({
      max: 3,
        autocomplete: {
          values: Object.keys(wordPool),
          only: true
        },
        destroy: function($elem) {
          if ($elem.tags.length < 1) {
            $("#stacked-selected-tag").val('');
            $("#drawing-selection").hide();
            currentTag = '';
          }
        },
        change: function($elem) {
          if (currentTag === '' && mode === -1){
            loop();
            pg.background('#ffffff');
            mode = 0;
          }
          if ($elem.tags.length > 0 && $elem.tags[0] != currentTag) {
            $elem.next().removeClass("alert-error"); //Remove error from div
            currentTag = $elem.tags[0];
            $("#stacked-selected-tag").val(currentTag);
            // wordPool is shared in wordPool.js
            let words = wordPool[currentTag];
            //https://stackoverflow.com/questions/19269545/how-to-get-a-number-of-random-elements-from-an-array
            let chosenWords =  words.sort(() => Math.random() - Math.random()).slice(0, 3);
            $("#drawing-word-1").val(chosenWords[0]);
            $("label[for='drawing-word-1']").text(chosenWords[0]);
            $("#drawing-word-2").val(chosenWords[1]);
            $("label[for='drawing-word-2']").text(chosenWords[1]);
            $("#drawing-word-3").val(chosenWords[2]);
            $("label[for='drawing-word-3']").text(chosenWords[2]);
            $("#drawing-selection").show();
          }
        },
        errors: { 
          empty: 'Input field is empty.',
          exists:'This tag already exists.',
          autocomplete_only: 'Please enter one of the suggested tags.',
          minLength: 'Your tag should have at least %s characters.',
          maxLength: 'Your tag should have at most %s characters.',
          max: 'The number of tags cannot exceed %s.'      
        }
    });
    
  }

function submitPost() {
  let valid = $('#drawing-title-form')[0].reportValidity();
  if (!$("#stacked-selected-tag").val()){
    $(".drawing-settings-box .inputTags-list").addClass("alert-error")
    valid = false;
  }
  
  if (valid){
    $("#dialog-text").text(`You will be able to edit the settings 
      and delete your post later, but you will not be 
      able to change your tags or redraw your post.`)
    let og = mode;
    mode = -1;
    $("#dialog-confirm").dialog({
      title: "Submit your post?",
      resizable: false,
      height: "auto",
      width: 400,
      modal: true,
      buttons: {
          "Submit": function() {
            saveCanvastoDataURL();
            $( this ).dialog( "close" );
          },
          Cancel: function() {
              setTimeout(() => mode=og, 200)
              $( this ).dialog( "close" );
          }
      }
    });
  }
}

function saveCanvastoDataURL() {
  // https://stackoverflow.com/questions/22409667/how-to-combine-two-javascript-formdata-objects
  let formData = new FormData($('#drawing-title-form')[0]);
  let poData = $('#drawing-settings-form').serializeArray();
  for (var i=0; i<poData.length; i++){
    formData.append(poData[i].name, poData[i].value)
  }
  formData.append("drawing_tags", $('#stacked-drawing-tags').val())

  canvas.canvas.toBlob(blob => {
    formData.append('post_image', blob);

    $.ajax({
      type: 'POST',
      url: "drawing",
      data: formData,
      processData: false,
      contentType: false,
      success: function(result){
        console.log(result)
        window.location.href ="/post/"+result;
      } 
    })
  })
}

function windowResized() {
  let width = div.offsetWidth * 0.95;
  let height = width * 0.75;
  width = Math.round(width);
  height = Math.round(height);
  
  canvas = resizeCanvas(width, height);
  var newPg = createGraphics(width, height);
  newPg.image(pg, 0, 0, width, height);
  pg = newPg;
}


function draw() {
  pg.strokeWeight(brushSize);
  if (mode == 0) {
    eraser.style('background-color', '#0c9b7e');
    pg.stroke(colorPicker.color());
    pg.fill(colorPicker.color());
  }
  else if (mode == 1) {
    eraser.style('background-color', 'orangered');
    pg.stroke('#ffffff');
    pg.fill('#ffffff');
  }
  image(pg, 0,0);
}

function mouseClicked(){
  if (mode != -1)
    pg.circle(mouseX,mouseY,1);
} 

function mouseDragged(){
  if (drawing && mode != -1){
    pg.line(mouseX, mouseY, pmouseX, pmouseY);
    return false;
  }
}

function mousePressed() {
  if (mouseX <= pg.width+30 && mouseX >= -30 && mouseY <= pg.height+30 && mouseY >= -30){
    drawing = 1;
  }
}

function mouseReleased() {
  drawing = 0;
}

function switchEraser() {
  if (mode !== -1) mode = !mode;
}

function resetCanvas() {
  $("#dialog-text").text(`Do you want to clear the canvas?`)
  let og = mode;
  mode = -1;
  $("#dialog-confirm").dialog({
    title: "Reset your drawing?",
    resizable: false,
    height: "auto",
    width: 400,
    modal: true,
    buttons: {
        Confirm: function() {
          pg.background('#ffffff');
          image(pg, 0,0);
          setTimeout(() => mode=og, 200)
          $( this ).dialog( "close" );
        },
        Cancel: function() {
            $( this ).dialog( "close" );
            setTimeout(() => mode=og, 200)
        }
    }
  });
}