function readNIFTI(data,canvas, slider) {
  
    var niftiHeader, niftiImage;

    // parse nifti
    if (nifti.isCompressed(data)) {
        data = nifti.decompress(data);
    }

    if (nifti.isNIFTI(data)) {
        niftiHeader = nifti.readHeader(data);
        niftiImage = nifti.readImage(niftiHeader, data);
    }

    // set up slider
    var slices = niftiHeader.dims[3];
    slider.max = slices - 1;
    slider.value = Math.round(slices / 2);
    slider.oninput = function() {
        drawCanvas(canvas, slider.value, niftiHeader, niftiImage);
    }; 
    // draw slice
    drawCanvas(canvas, slider.value, niftiHeader, niftiImage);
}

/**
 * 
 * @param typedData les données d'une image de segmentation
 * @returns les classes [0,1,2,3,4..] présentes dans l'image
 */
function classesDeSegmentation(typedData){
    let unique = [...new Set(typedData)];
    return unique;
}


function drawCanvas(canvas, slice, niftiHeader, niftiImage) {
    isAsegmentationFile = false;
    // console.log(niftiHeader)
    // console.log(niftiImage)
    // get nifti dimensions
    var cols = niftiHeader.dims[1];
    var rows = niftiHeader.dims[2];
    
    // set canvas dimensions to nifti slice dimensions
    canvas.width = cols;
    canvas.height = rows;
    
    // make canvas image data
    var ctx = canvas.getContext("2d");
    var canvasImageData = ctx.createImageData(canvas.width, canvas.height);
    
    // convert raw data to typed array based on nifti datatype
    var typedData;
    

    if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT8) {
        typedData = new Uint8Array(niftiImage);
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT16) {
        typedData = new Int16Array(niftiImage);
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT32) {
        typedData = new Int32Array(niftiImage);
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_FLOAT32) { // Par ici que passent les fichiers d'anatomie
        typedData = new Float32Array(niftiImage);
        isAsegmentationFile =false;
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_FLOAT64) {
        typedData = new Float64Array(niftiImage);
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT8) {
        typedData = new Int8Array(niftiImage);
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT16) { // Par ici que passent les fichiers de segmentation
        typedData = new Uint16Array(niftiImage);
        isAsegmentationFile =true;
        classesSegmentation = [0,1,2,3,4]; // Les différentes classes possibles (et qui seront rendues par l'IA). si doute, appeler classesDeSegmentation
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT32) {
        typedData = new Uint32Array(niftiImage);
    } else {
        return;
    }
   
    // offset to specified slice
    var sliceSize = cols * rows;
    var sliceOffset = sliceSize * slice;
    
    // draw pixels
    for (var row = 0; row < rows; row++) {
        var rowOffset = row * cols;
        var colsnumber  = parseInt(""+cols);
        for (var col = 0; col < colsnumber; col++) {
            var offset = sliceOffset + rowOffset + col;
            var value = typedData[offset];  
            if(isAsegmentationFile && value!==0){
                value= value * (255/classesSegmentation.length);
            }
            canvasImageData.data[(rowOffset + col) * 4] = value & 0xFF;
            canvasImageData.data[(rowOffset + col) * 4 + 1] = value & 0xFF;
            canvasImageData.data[(rowOffset + col) * 4 + 2] = value & 0xFF;
            canvasImageData.data[(rowOffset + col) * 4 + 3] = 0xFF;
        }
    }

    
    ctx.putImageData(canvasImageData, 0, 0);
}

function makeSlice(file, start, length) {
    var fileType = (typeof File);

    if (fileType === 'undefined') {
        return function () { };
    }

    if (File.prototype.slice) {
        return file.slice(start, start + length);
    }

    if (File.prototype.mozSlice) {
        return file.mozSlice(start, length);
    }

    if (File.prototype.webkitSlice) {
        return file.webkitSlice(start, length);
    }

    return null;
}

function readFile(file,canvas, slider) {
    var blob = makeSlice(file, 0, file.size);
    var reader = new FileReader();

    reader.onloadend = function (evt) {
        if (evt.target.readyState === FileReader.DONE) {
            readNIFTI(evt.target.result,canvas, slider);
        }
    };

    reader.readAsArrayBuffer(blob);
}

function handleFileSelect(files,idCanvas,idSlider) {
    var canvas = document.getElementById(idCanvas);
    var slider = document.getElementById(idSlider);
    if(files.length>0 && slider!==null && canvas!==null) readFile(files[0],canvas,slider);
}

function resetCanvas(idCanvas,idSlider){
  let canvas = document.getElementById(idCanvas)
  const context = canvas.getContext('2d');
  context.reset();
  let slider = document.getElementById(idSlider);
  slider.value =  (+slider.max+(+slider.min))/2;
  slider.oninput = function() {}
}