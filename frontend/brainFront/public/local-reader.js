/**
 * 
 * @param typedData les données d'une image de segmentation
 * @returns les classes [0,1,2,3,4..] présentes dans l'image
 */
function classesDeSegmentation(typedData){
    let unique = [...new Set(typedData)];
    return unique;
}

function getTypedData(niftiHeader,niftiImage){
    let isAsegmentationFile = false;
    let typedData;
    
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
        classesSegmentation = classesDeSegmentation(typedData); // Les différentes classes possibles 
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT32) {
        typedData = new Uint32Array(niftiImage);
    } 
    return {typedData,isAsegmentationFile};
}

function readNIFTI(data,canvas, slider,coupe) {
  
    var niftiHeader, niftiImage;

    // parse nifti
    if (nifti.isCompressed(data)) {
        data = nifti.decompress(data);
    }

    if (nifti.isNIFTI(data)) {
        niftiHeader = nifti.readHeader(data);
        niftiImage = nifti.readImage(niftiHeader, data);
    }

    
    let typed = getTypedData(niftiHeader,niftiImage);
    let typedData = typed.typedData;
    let isAsegmentationFile = typed.isAsegmentationFile;

    slider.value = 0.5 *slider.max;
    
    slider.oninput = function() { // L'image sera recalculée à chaque mouvement du slider
        drawCanvas(canvas, slider.value/slider.max, niftiHeader, typedData,isAsegmentationFile,coupe);
    }; 
    // Affiche image initiale
    drawCanvas(canvas, 0.5, niftiHeader, typedData,isAsegmentationFile,coupe);   
}

function drawCanvas(canvas, slice, niftiHeader, typedData, isAsegmentationFile,coupe="axiale") {

    let dimA = niftiHeader.dims[1];
    let dimB = niftiHeader.dims[2]; 
    let dimC = niftiHeader.dims[3];
    // get nifti dimensions
    
    // set canvas dimensions to nifti slice dimensions
    canvas.width = dimA;
    canvas.height = dimB;
    
    // slice est un chiffre entre 0 et 1, on le remet aux dimensions de la coupe.
    slice= Math.floor(slice*dimC); 
   // if(coupe==="sagitalle")slice= Math.floor(slice*dimA);

    
    // make canvas image data
    var ctx = canvas.getContext("2d");
    var canvasImageData = ctx.createImageData(canvas.width, canvas.height);

    let currentview = loadAxialView(slice,dimA,dimB,typedData);
    //TODO: appeler loadSagitalView & load CoronalView lorsque l'on aura compris comment faire
    
    // display current view
    for(let i=0;i<currentview.length;i++){
        let row = currentview[i];
        for(let j=0;j<row.length;j++){
            let value = row[j];
            if(isAsegmentationFile && value!==0 && value!==undefined){
                rgbValue = selectColor(classesSegmentation.indexOf(value)/classesSegmentation.length)
                canvasImageData = setPixelValue((i * dimA)+j,canvasImageData,rgbValue.r,rgbValue.g,rgbValue.b,255);
            }
            else {
                canvasImageData = setPixelValue((i * dimA) + j,canvasImageData,value,value,value,255)
            }
        }
    }
 //   console.log(currentview)
    ctx.putImageData(canvasImageData, 0, 0);
}

function loadAxialView(slice,dimA, dimB,typedData){
    let axial = []
    let start = (dimA*dimB)*(slice);
    let currentRow = []
    for(let i=0;i<(dimA*dimB);i++){
        let offset = i+ start;
        var value = typedData[offset];  
        currentRow.push(value);
        if(currentRow.length==dimA){
            axial.push(currentRow);
            currentRow = []
        }
    }
    return axial;
}

//4435200, 4435201, 4435202, 4435203, 4435204, 4435205, 4435206, 4435207, 4435208, 4435209, 4435210, 4435211, 4435212, 4435213, 4435214, 4435215, 4435216, 4435217, 4435218, 4435219, 4435220, 4435221, 4435222, 4435223, 4435224, 4435225, 4435226, 4435227, 4435228, 4435229, 4435230, 4435231, 4435232, 4435233, 4435234, 4435235, 4435236, 4435237, 4435238, 4435239, 4435240, 4435241, 4435242, 4435243, 4435244, 4435245, 4435246, 4435247, 4435248, 4435249, 4435250, 4435251, 4435252, 4435253, 4435254, 4435255, 4435256, 4435257, 4435258, 4435259, 4435260, 4435261, 4435262, 4435263, 4435264, 4435265, 4435266, 4435267, 4435268, 4435269, 4435270, 4435271, 4435272, 4435273, 4435274, 4435275, 4435276, 4435277, 4435278, 4435279, 4435280, 4435281, 4435282, 4435283, 4435284, 4435285, 4435286, 4435287, 4435288, 4435289, 4435290, 4435291, 4435292, 4435293, 4435294, 4435295, 4435296, 4435297, 4435298, 4435299
//4492799


function selectColor(perct,palette_index=0){
   dutch_field_palette = [[230, 0, 73], [11, 180, 255], [80, 233, 145], [230, 215, 0],[155, 25, 245], [255, 163, 0], [220, 10, 181], [179, 212, 255], [0, 191, 159]]
    blue_yellow_palette =  [[17, 95, 154], [25, 131, 197], [34, 167, 240],[72, 181, 196] , [118, 198, 143], [166, 215, 91], [202, 229, 47], [208, 238, 17], [244, 240, 0]]
    blue_red_palette = [[25, 132, 197],[34, 168, 240], [99, 191, 240], [167, 213, 237], [226, 226, 226], [225, 166, 146], [222, 110, 86], [225, 75, 49], [194, 55, 40]]
    palette = [dutch_field_palette,blue_yellow_palette,blue_red_palette][palette_index]
    value_index = Math.floor(perct*(palette.length-1));
    value = palette[value_index]
    return {"r":value[0],"g":value[1],"b":value[2]};
}

function setPixelValue(index,canvasImageData,red,green,blue,opacity){
    canvasImageData.data[index * 4] = red & 0xFF;
    canvasImageData.data[index * 4 + 1] = green & 0xFF;
    canvasImageData.data[index * 4 + 2] = blue & 0xFF;
    canvasImageData.data[index * 4 + 3] = opacity & 0xFF;
    return canvasImageData;
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

function readFile(file,canvas, slider,coupe) {
    var blob = makeSlice(file, 0, file.size);
    var reader = new FileReader();

    reader.onloadend = function (evt) {
        if (evt.target.readyState === FileReader.DONE) {
            readNIFTI(evt.target.result,canvas, slider,coupe);
        }
    };

    reader.readAsArrayBuffer(blob);
}

function handleFileSelect(files,idCanvas,idSlider,coupe) {
    var canvas = document.getElementById(idCanvas);
    var slider = document.getElementById(idSlider);
    if(files.length>0 && slider!==null && canvas!==null) readFile(files[0],canvas,slider,coupe);
}

function resetCanvas(idCanvas,idSlider){
  let canvas = document.getElementById(idCanvas)
  const context = canvas.getContext('2d');
  context.reset();
  let slider = document.getElementById(idSlider);
  slider.value =  (+slider.max+(+slider.min))/2;
  slider.oninput = function() {}
}