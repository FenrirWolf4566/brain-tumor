
/*jslint browser: true, node: true */
/*global require, module */

"use strict";

/*** Imports ***/

var nifti = nifti || {};
nifti.Utils = nifti.Utils || {};
nifti.NIFTIEXTENSION = nifti.NIFTIEXTENSION || ((typeof require !== 'undefined') ? require('./nifti-extension.js') : null);


/*** Static Pseudo-constants ***/

nifti.Utils.crcTable = null;
nifti.Utils.GUNZIP_MAGIC_COOKIE1 = 31;
nifti.Utils.GUNZIP_MAGIC_COOKIE2 = 139;



/*** Static methods ***/

nifti.Utils.getStringAt = function (data, start, end) {
    var str = "", ctr, ch;

    for (ctr = start; ctr < end; ctr += 1) {
        ch = data.getUint8(ctr);

        if (ch !== 0) {
            str += String.fromCharCode(ch);
        }
    }

    return str;
};



nifti.Utils.getByteAt = function (data, start) {
    return data.getInt8(start);
};



nifti.Utils.getShortAt = function (data, start, littleEndian) {
    return data.getInt16(start, littleEndian);
};



nifti.Utils.getIntAt = function (data, start, littleEndian) {
    return data.getInt32(start, littleEndian);
};



nifti.Utils.getFloatAt = function (data, start, littleEndian) {
    return data.getFloat32(start, littleEndian);
};



nifti.Utils.getDoubleAt = function (data, start, littleEndian) {
    return data.getFloat64(start, littleEndian);
};



nifti.Utils.getLongAt = function (data, start, littleEndian) {
    var ctr, array = [], value = 0;

    for (ctr = 0; ctr < 8; ctr += 1) {
        array[ctr] = nifti.Utils.getByteAt(data, start + ctr, littleEndian);
    }

    for (ctr = array.length - 1; ctr >= 0; ctr--) {
        value = (value * 256) + array[ctr];
    }

    return value;
};

nifti.Utils.getExtensionsAt = function (data, start, littleEndian, voxOffset) {
    let extensions = [];
    let extensionByteIndex = start;

    // Multiple extended header sections are allowed
    while(extensionByteIndex < voxOffset ) {
        // assume same endianess as header until proven otherwise
        let extensionLittleEndian = littleEndian;
        let esize = nifti.Utils.getIntAt(data, extensionByteIndex, littleEndian);
        if(!esize) {
            break; // no more extensions
        }
        
        // check if this takes us past vox_offset
        if(esize + extensionByteIndex > voxOffset) {
            // check if reversing byte order gets a proper size
            extensionLittleEndian = !extensionLittleEndian;
            esize = nifti.Utils.getIntAt(data, extensionByteIndex, extensionLittleEndian);
            if(esize + extensionByteIndex > voxOffset) {
                throw new Error('This does not appear to be a valid NIFTI extension');
            }
        }

        // esize must be a positive integral multiple of 16
        if(esize % 16 != 0) {
            throw new Error("This does not appear to be a NIFTI extension");
        }

        let ecode = nifti.Utils.getIntAt(data, extensionByteIndex + 4, extensionLittleEndian);
        let edata = data.buffer.slice(extensionByteIndex + 8, extensionByteIndex + esize);
        console.log('extensionByteIndex: ' + (extensionByteIndex + 8) + ' esize: ' + esize);
        console.log(edata);
        let extension = new nifti.NIFTIEXTENSION(esize, ecode, edata, extensionLittleEndian);
        extensions.push(extension);
        extensionByteIndex += esize; 
    }
    return extensions;
}


nifti.Utils.toArrayBuffer = function (buffer) {
    var ab, view, i;

    ab = new ArrayBuffer(buffer.length);
    view = new Uint8Array(ab);
    for (i = 0; i < buffer.length; i += 1) {
        view[i] = buffer[i];
    }
    return ab;
};



nifti.Utils.isString = function (obj) {
    return (typeof obj === "string" || obj instanceof String);
};


nifti.Utils.formatNumber = function (num, shortFormat) {
    var val = 0;

    if (nifti.Utils.isString(num)) {
        val = Number(num);
    } else {
        val = num;
    }

    if (shortFormat) {
        val = val.toPrecision(5);
    } else {
        val = val.toPrecision(7);
    }

    return parseFloat(val);
};



// http://stackoverflow.com/questions/18638900/javascript-crc32
nifti.Utils.makeCRCTable = function(){
    var c;
    var crcTable = [];
    for(var n =0; n < 256; n++){
        c = n;
        for(var k =0; k < 8; k++){
            c = ((c&1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1));
        }
        crcTable[n] = c;
    }
    return crcTable;
};



nifti.Utils.crc32 = function(dataView) {
    var crcTable = nifti.Utils.crcTable || (nifti.Utils.crcTable = nifti.Utils.makeCRCTable());
    var crc = 0 ^ (-1);

    for (var i = 0; i < dataView.byteLength; i++ ) {
        crc = (crc >>> 8) ^ crcTable[(crc ^ dataView.getUint8(i)) & 0xFF];
    }

    return (crc ^ (-1)) >>> 0;
};



/*** Exports ***/

var moduleType = typeof module;
if ((moduleType !== 'undefined') && module.exports) {
    module.exports = nifti.Utils;
}
