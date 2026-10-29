let port, writer, reader, textDecoder, readableStreamClosed, isConnected = false, espBtnProgress;
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

async function connectSerial(fileName, buttonElement) {
    espBtnProgress = buttonElement.children[0];
    if (navigator.serial) {
        try {
            port = await navigator.serial.requestPort();
            await port.open({ baudRate: 115200 });
            writer = port.writable.getWriter();
            textDecoder = new TextDecoderStream();
            readableStreamClosed = port.readable.pipeTo(textDecoder.writable);
            reader = textDecoder.readable.getReader();
            isConnected = true;
            uploadLibrariesSerial(fileName);
        } catch (error) {
            console.error("Error in connectSerial:", error);
        }
    } else {
        alert("Web Serial API not supported.");
    }
}

async function connectSerialMultiple(fileNames, buttonElement) {
    espBtnProgress = buttonElement.children[0];
    if (navigator.serial) {
        try {
            port = await navigator.serial.requestPort();
            await port.open({ baudRate: 115200 });
            writer = port.writable.getWriter();
            textDecoder = new TextDecoderStream();
            readableStreamClosed = port.readable.pipeTo(textDecoder.writable);
            reader = textDecoder.readable.getReader();
            isConnected = true;
            await uploadLibrariesSerialMultiple(fileNames);
        } catch (error) {
            console.error("Error in connectSerialMultiple:", error);
        }
    } else {
        alert("Web Serial API not supported.");
    }
}

async function disconnectSerial() {
    try {
        await writeSerial("04");
        reader.cancel();
        reader.releaseLock();
        await readableStreamClosed.catch(() => {});
        writer.releaseLock();
        await port.close();
        isConnected = false;
        espBtnProgress.innerText = " done!";
    } catch (error) {
        console.log(error);
    }
}

async function writeSerial(command) {
    let data;
    switch (command) {
        case "01":
            data = new Uint8Array([1]);
            break;
        case "02":
            data = new Uint8Array([2]);
            break;
        case "03":
            data = new Uint8Array([3]);
            break;
        case "04":
            data = new Uint8Array([4]);
            break;
        default:
            return;
    }
    await writer.write(data);
    await wait(10);
}

async function enterRawREPL() {
    await writeSerial("03");
    await writeSerial("03");
    for (let i = 0; i < 5; i++) {
        await writeSerial("01");
    }
    await writeSerial("04");
    await writeSerial("03");
    await writeSerial("03");
}

async function exitRawREPL() {
    await writeSerial("02");
}

async function saveLibrary(code, fileName) {
    await enterRawREPL();
    await executeRawNoFollow(`f = open('${fileName}', 'wb')`);
    code = code.replace(/(\r\n|\n|\r)/gm, "£").replace(/"/g, '\\"');

    for (let i = 0; i < code.length; i += 310) {
        let chunk = code.slice(i, Math.min(i + 310, code.length));
        await executeRawNoFollow(`f.write("${chunk.replace(/£/g, "\\n")}")`);
        let progress = Math.min((i + 310) / code.length * 100, 100);
        espBtnProgress.textContent = ` ${Math.floor(progress)}%`;
        await wait(100);
    }
    await executeRawNoFollow("f.close()");
    await exitRawREPL();
}

async function executeRawNoFollow(command) {
    const encoder = new TextEncoder();
    const encodedCommand = encoder.encode(command);
    for (let i = 0; i < encodedCommand.length; i += 32) {
        const chunk = encodedCommand.slice(i, Math.min(i + 32, encodedCommand.length));
        await writer.write(chunk);
        await wait(50);
    }
    await writeSerial("04");
}

async function uploadLibrariesSerial(fileName) {
    try {
        const response = await fetch("./codes/" + fileName + "?v=" + Date.now(), { cache: "no-store" });
        const code = await response.text();
        await saveLibrary(code, "main.py");
        disconnectSerial();
    } catch (error) {
        console.error(error);
    }
}


async function uploadLibrariesSerialMultiple(fileNames) {
    try {
        for (let i = 0; i < fileNames.length; i++) {
            const sourceName = fileNames[i].replace(/\.py$/, '.txt');
            const response = await fetch("./libraries/" + sourceName + "?v=" + Date.now(), { cache: "no-store" });
            const code = await response.text();
            // Save with its .py name on the device
            await saveLibrary(code, fileNames[i]);
            let progress = Math.floor(((i + 1) / fileNames.length) * 100);
            espBtnProgress.textContent = ` ${progress}%`;
        }
        disconnectSerial();
    } catch (error) {
        console.error(error);
    }
}
