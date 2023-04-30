const classNames = { "4": "Tumeur GD rehaussée", "2": "œdème péritumoral", "1": "cœur de tumeur nécrosé non rehaussé" };
/**
 * 
 * @param typedData les données d'une image de segmentation
 * @returns les classes [0,1,2,3,4..] présentes dans l'image
 */
function classesDeSegmentation(typedData) {
    let unique = [...new Set(typedData)];
    return unique;
}

function getTypedData(niftiHeader, niftiImage) {
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
        isAsegmentationFile = false;
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_FLOAT64) {
        typedData = new Float64Array(niftiImage);
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_INT8) {
        typedData = new Int8Array(niftiImage);
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT16) { // Par ici que passent les fichiers de segmentation
        typedData = new Uint16Array(niftiImage);
        isAsegmentationFile = true;
    } else if (niftiHeader.datatypeCode === nifti.NIFTI1.TYPE_UINT32) {
        typedData = new Uint32Array(niftiImage);
    }
    return { typedData, isAsegmentationFile };
}

function getImage(dim, slice, array, header) {
    slice /= 100;
    let image
    if (dim === 1) {
        slice = Math.floor(slice * header.dims[1]);
        image = array.pick(slice, null, null)
    } else if (dim === 2) {
        slice = Math.floor(slice * header.dims[2]);
        image = array.pick(null, slice, null)
    } else if (dim === 3) {
        slice = Math.floor(slice * header.dims[3]);
        image = array.pick(null, null, header.dims[3] - slice - 1)
    }
    return image
}

function loadNiftiFile(data) {
    let niftiHeader, niftiImage;
    // parse nifti
    if (nifti.isCompressed(data)) {
        data = nifti.decompress(data);
    }
    if (nifti.isNIFTI(data)) {
        niftiHeader = nifti.readHeader(data);
        niftiImage = nifti.readImage(niftiHeader, data);
    }
    let typed = getTypedData(niftiHeader, niftiImage);
    let typedData = typed.typedData;
    let isAsegmentationFile = typed.isAsegmentationFile;
    let classesSegmentation = [];
    if(isAsegmentationFile)classesSegmentation = classesDeSegmentation(typedData); // Les différentes classes possibles
    let dims = niftiHeader.dims
    //compute voxel intensity range
    let mn = typedData[0];
    let mx = mn;
    for (let i = 0; i < (dims[1] * dims[2] * dims[3]); i++) {
        mn = Math.min(mn, typedData[i]);
        mx = Math.max(mx, typedData[i]);
    }
    // special case (to avoid dividing by 0)
    if(mn==mx){ 
        mx = mn+1;
    }
    //console.log('Voxel intensity range ', typedData[0], mn, mx);
    // set slope and intercept to convert range to 0..255, 
    niftiHeader.displayIntercept = mn; //make darkest value 0
    niftiHeader.displaySlope = 255.0 / (mx - mn); //make brightest value 255
    //
    let stride = [1, dims[1], dims[1] * dims[2]]
    let array = ndarray(typedData, [dims[1], dims[2], dims[3]], stride).step(1, 1, -1);
    return {"data":array,"header":niftiHeader,"isSegmentation":isAsegmentationFile,"classesSegmentation":classesSegmentation};
}



function drawNiftiFiles(canvas,niftifiles,nomcoupe,slice){
    canvas.style.backgroundColor = 'black';
    let coupeId = nomcoupe == "axiale" ? 3 : nomcoupe == "sagittale" ? 1 : 2;
    let cols = niftifiles[0].header.dims[1];
    let rows = niftifiles[0].header.dims[2];
    canvas.width = cols;
    canvas.height =rows;
    let ctx = canvas.getContext("2d",{willReadFrequently: true});
    let canvasImageData = ctx.createImageData(canvas.width, canvas.height);


    const filesSeg = niftifiles.filter(file => file.isSegmentation);
    const filesAnat = niftifiles.filter(file => !file.isSegmentation);

    const imagesSeg = filesSeg.map(file=>{ return getImage(coupeId,slice,file.data,file.header);});
    const imagesAnat = filesAnat.map(file=>{ return getImage(coupeId,slice,file.data,file.header);});

    // Sélection de l'image de segmentation 
    // (on n'en prend qu'une pour une meilleure cohérence)
    // Celle que l'on choisit est celle avec l'opacité la plus élevée
    // Si plusieurs ont cette même opacité, on prend la dernière
    let maxOpSeg =  Math.max(...filesSeg.map(file=>{return file.opacity}));
    let imgSeg = undefined;
    let fileSeg = undefined;
    for(let i=0;i<filesSeg.length;i++){
        if(filesSeg[i].opacity==maxOpSeg){
            imgSeg=imagesSeg[i];
            fileSeg = filesSeg[i];
        }
    }
    
    for (let row = 0; row < rows; row++) {
        let rowOffset = row * cols;
        for (let col = 0; col < cols; col++) {
            // Calque pixel par pixel selon la nature des images
            let anatValue = undefined;
            let anatOpac = undefined;
            // Traitement de la valeur du pixel selon les Images d'anatomie
            if(imagesAnat.length>0){
                let values = imagesAnat.map((image,index)=>{
                    let niftiHeader = filesAnat[index].header;
                    let op = filesAnat[index].opacity/255;
                    return  op*(image.get(col,row)-niftiHeader.displayIntercept) * niftiHeader.displaySlope;
                });
                let value = Math.max(...values)
                let opacities = filesAnat.map(file=>{return file.opacity;})
                let opacity = Math.max(...opacities); 
                canvasImageData = setPixelValue(rowOffset + col, canvasImageData, value, value, value, opacity);
                anatValue = value;
                anatOpac = opacity;
            }

            // Traitement de la valeur du pixel selon les Images de segmentation
            if(imgSeg!==undefined){
                let value = imgSeg.get(col,row);
                let opacity = fileSeg.opacity;
                if(value!==0 && value!==undefined){
                    let rgbValue = selectColor(fileSeg.classesSegmentation.indexOf(value));
                    if(anatOpac!==undefined && anatValue!==undefined){
                        // Gestion de l'opacité de l'image de segmentation
                        let alpha = opacity /255;
                        let r = (1 - alpha)*anatValue + alpha*rgbValue.r;
                        let g = (1 - alpha)*anatValue + alpha*rgbValue.g;
                        let b = (1 - alpha)*anatValue + alpha*rgbValue.b;
                       rgbValue = {r,g,b};
                    }
                    canvasImageData = setPixelValue(rowOffset + col, canvasImageData, rgbValue.r, rgbValue.g, rgbValue.b, 255);
                }
            }
    
        }
    }
    ctx.putImageData(canvasImageData, 0, 0);
}


function removeLegend() {
    let doc = document.getElementById('legend');
    if (doc != undefined) {
        doc.innerHTML = "";
    }
}

function createLegend(classesSegmentation) {
    classesSegmentation = classesSegmentation.sort()
    palette = ["#ffbd99", "#ff0000", "#ffff00", "#e2adf2"]
    let doc = document.getElementById('legend');
    if (doc.childElementCount == 0) { //éviter les duplicats lors du changement de couleur
        let content = "<h3>Légende</h3> <div id='bodylegend'>";
        for (let classe of classesSegmentation) {
            if (+classe !== 0) { // On ne gère pas la couleur du fond
                let color = palette[(+classe) % palette.length];
                nom = 'Classe ' + classe;
                if (classNames[classe] !== undefined) nom = classNames[classe];
                content += "<div class='duocolor'>";
                content += '<span class="dot" ><input type="color" id="dot-class' + classesSegmentation.indexOf(classe) + '" value="' + color + '"></span>';
                content += '<span class="classname">' + nom + '</span></div>';
            }
        }
        content += "</div>"
        doc.innerHTML += content;
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
function selectColor(idclasse) {
    value = document.getElementById('dot-class' + idclasse).value
    return hexToRgb(value);
}


function setPixelValue(index, canvasImageData, red, green, blue, opacity) {
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

function readFile(file, canvas, slider, coupe,keeplegend=true,opacityslider=undefined) {
    let blob = makeSlice(file, 0, file.size);
    let reader = new FileReader();

    reader.onloadend = function (evt) {
        if (evt.target.readyState === FileReader.DONE) {
            readNIFTI(evt.target.result, canvas, slider, coupe,keeplegend,opacityslider);
        }
    };

    reader.readAsArrayBuffer(blob);
}
function readNiftiFile(file) {
    return new Promise((res) => {
      let blob = makeSlice(file, 0, file.size);
      let reader = new FileReader();
      reader.readAsArrayBuffer(blob);
  
      reader.onloadend = function (evt) {
        if (evt.target.readyState === FileReader.DONE) {
          let nfti = loadNiftiFile(evt.target.result);
          res(nfti);
        }
      };
    });
  }


function resetCanvas(idCanvas, idSlider) {
    let slider = document.getElementById(idSlider);
    slider.value = 50;
    let canvas = document.getElementById(idCanvas)
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    canvas.style.backgroundColor='transparent';
    removeLegend();
}