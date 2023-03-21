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
        removeLegend();
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_FLOAT64) {
        typedData = new Float64Array(niftiImage);
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT8) {
        typedData = new Int8Array(niftiImage);
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT16) { // Par ici que passent les fichiers de segmentation
        typedData = new Uint16Array(niftiImage);
        isAsegmentationFile =true;
        classesSegmentation = classesDeSegmentation(typedData); // Les différentes classes possibles
        createLegend(classesSegmentation); 
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT32) {
        typedData = new Uint32Array(niftiImage);
    } 
    return {typedData,isAsegmentationFile};
}

function getImage(dim, slice, array,header){
    slice /=100;
    let image
    if (dim === 1) {
        slice = Math.floor(slice*header.dims[1]);
        image = array.pick(slice, null, null)
    } else if (dim === 2) {
        slice = Math.floor(slice*header.dims[2]);
        image = array.pick(null, slice, null)
    } else if (dim === 3) {
        slice = Math.floor(slice*header.dims[3]);
        image = array.pick(null, null, header.dims[3] - slice - 1)
    }
    return image
}

function readNIFTI(data,canvas, slider,coupe) {
    let coupeId = coupe=="axiale"?3:coupe=="sagittale"?1:2;
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
    let dims = niftiHeader.dims
    let stride = [1, dims[1], dims[1] * dims[2]]
    let array = ndarray(typedData, [dims[1], dims[2], dims[3]], stride).step(1, 1, -1) 
    
    slider.value = (0.5 *(+slider.max));
    let draw =function() { drawIt(canvas,niftiHeader,getImage(coupeId,+slider.value,array,niftiHeader),isAsegmentationFile)}; 
    // L'image sera recalculée à chaque mouvement du slider
    slider.oninput = draw;
    if(isAsegmentationFile){
        let colorinputs = document.getElementsByClassName('dot');
        for(let col of colorinputs){
            col.oninput =draw;
        }
    }
    // Affiche image initiale  
    draw();
}


function drawIt(canvas,niftiHeader,image,isAsegmentationFile){
    let cols = niftiHeader.dims[1];
    let rows = niftiHeader.dims[2];
    canvas.width = cols;
    canvas.height = rows;
    var ctx = canvas.getContext("2d");
    var canvasImageData = ctx.createImageData(canvas.width, canvas.height);
    for (let row = 0; row < rows; row++) {
        let rowOffset = row * cols;
        for (let col = 0; col < cols; col++) {
            let value = image.get(col, row)
            if(isAsegmentationFile && value!==0 && value!==undefined){
                rgbValue = selectColor(classesSegmentation.indexOf(value))
                canvasImageData = setPixelValue(rowOffset+col,canvasImageData,rgbValue.r,rgbValue.g,rgbValue.b,255);
            }
            else {
                canvasImageData = setPixelValue(rowOffset+col,canvasImageData,value,value,value,255)
            }
        }
    }
    ctx.putImageData(canvasImageData, 0, 0);
}

function removeLegend(){
    let doc = document.getElementById('legend');
    if(doc!=undefined){
        doc.innerHTML="";
    }
}

function createLegend(classesSegmentation){
    palette = ["#F87060","#8AE9C1","#801a86","#e2adf2"]
    let doc = document.getElementById('legend');
    if(doc.childElementCount==0){ //éviter les duplicats lors du changement de couleur
        let content = "<h3>Légende</h3> <div id='bodylegend'>";
        for(let idclasse in classesSegmentation){
            if(+idclasse!==0){ // On ne gère pas la couleur du fond
                content+="<div class='duocolor'>";
                content+='<span class="dot" ><input type="color" id="dot-class'+idclasse+'" value="'+palette[idclasse%palette.length]+'"></span>';
                content+='<span class="classname">Classe '+idclasse+'</span></div>';
            }
        }
        content+="</div>"
        doc.innerHTML+=content;
    }
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  }
function selectColor(idclasse){
    value = document.getElementById('dot-class'+idclasse).value
    return hexToRgb(value);
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