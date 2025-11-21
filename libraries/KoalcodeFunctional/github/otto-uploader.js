let port;
let writer;
let reader;
let textDecoder;
let readableStreamClosed;
let writableStreamClosed;
let isConnected = false;
var readValue = "";
var files = "";
var fileInput = "";
var isFiles = false;
var isFileInput = false;
var webreplActive = true;
var isMicropython = false;
var isCheckFilesCorrect = false;
var connectionType = "Serial";
var ottoLibraryFiles = ["adxl345.py", "ottoneopixel.py", "ottobuzzer.py", "ottomotor.py", "ottooled.py", "ottosensors.py", "ssd1306.py"];

var index = 0;
var termValue

let versionAlreadyChecked = false;
let initialVersionCheckDone = false;

const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

async function connectSerial() {

  if (navigator.serial) {
    
      try 
      {
        port = await navigator.serial.requestPort();
        await port.open({ baudRate: 115200 });
        writer = port.writable.getWriter();
        textDecoder = new TextDecoderStream();
        readableStreamClosed = port.readable.pipeTo(textDecoder.writable);
        reader = textDecoder.readable.getReader();
        let buffer = '';

        ConnectedSerialPort();
        sendCommand('print("isMicropython")');
        
        setTimeout(IsMicropython, 2000);
        setTimeout(checkMicropythonVersion, 2500);
        setTimeout(ShowOttoFilesCommand, 3000);

        try
        {
          //ShowOttoFileInput("boot.py");
        }
        catch
        {

        }
        
        while (true) {
          const { value, done } = await reader.read();
          if (done) {
            // Allow the serial port to be closed later.
            reader.releaseLock();
            break;
          }
          
          try
          {     
            buffer += value; // Gelen veriyi buffer'a ekle

            let endIndex;
            var fullMessage;

            //SerialData(buffer);

            while ((endIndex = buffer.indexOf('\n')) >= 0) {
              fullMessage = buffer.substring(0, endIndex).trim(); // Sonlandırıcıya kadar olan kısmı al
              //console.log('Full Message:', fullMessage);
              buffer = buffer.substring(endIndex + 1); // Kalan buffer'ı güncelle
            }

            SerialData(fullMessage);

            var termValue = value;
            termValue = MessagePrepare(termValue);
            console.log(termValue);

            if(window.localStorage.getItem("Page") == "Vertical")
              term.write(termValue);

          	/*
            if(window.localStorage.getItem("Page") == "Horizontal")
            {
              if(fullMessage.indexOf("#") > 0)
              {
                var dist = fullMessage.replace("D#", "").replace("$", "");
                dist = dist.substring(0, 5);
                $("#lbDistance").text(dist);
              }
            }
            */

            if(isFileInput == false && fullMessage != undefined)
            {
              if((fullMessage.toUpperCase().indexOf("ERROR") >= 0) && fullMessage.indexOf("_boot.py") < 0)
              {
                //console.log(fullMessage);
                //showModalDialog(ErrorText + "\n" + fullMessage, "error");
              }
            }

            if(fullMessage.indexOf("Micropython"))
            {
              isMicropython = true;
            }
          
            //WifiMessages();
          }
          catch(err)
          {
            console.log(err.message);
          }
        }
        
      } catch (err) {
        console.log(err)
        showModalDialog(SerialPortErrorText, "error");
        DisconnectedSerialPort();
      }

    } else {
      showModalDialog(WebApiNotSupportedText, "error");
    }
}

function IsMicropython() 
{ 
   if(isMicropython == false)
      showConfirmFirmware();
}

function compareArrays(arr1, arr2) {
    return arr2.filter(item => !arr1.includes(item)).join('\n');
}

function MessagePrepare(message)
{
    if(message == null || message == undefined)
      return "";

    if(message.indexOf('@') >= 0)
    { 
      isFiles = true;
      files = "";
    }

    if(message.indexOf('?') >= 0)
    { 
      isFileInput = true;
      fileInput = "";
      editorFileInput.setValue("");
    }
    
    if(isFileInput)
    {
      fileInput += message;
    }

    if(isFiles)
    {
      files += message;
      if(files.indexOf("@") >= 0 && files.indexOf("|") >= 0)
      {
        files = files.substring(files.indexOf("@") + 1, files.indexOf("|") - 1);

        var filesArray = files.split("\r\n");
        var fileHTML = "";

        for(var i = 1; i < filesArray.length; i++)
        {
          filesArray[i] = filesArray[i].replace("/", "").replace("\r", "");
        }

        if(isCheckFilesCorrect == false)
        {
            isCheckFilesCorrect = true;
            console.log(filesArray);
            console.log(ottoLibraryFiles);

            var missingLibraries = compareArrays(filesArray, ottoLibraryFiles);

            //if(missingLibraries != ""){
              //showModalDialog("There is missing library files\n " + missingLibraries, "info");
            //} 
        }

        for(var i = 1; i < filesArray.length; i++)
        {
          filesArray[i] = filesArray[i].replace("\n", "").replace("\r", "").replace("/", "");
          if(filesArray[i] != "directory.py" && filesArray[i] != "boot.py" && filesArray[i].indexOf(".py") > 0)
          {
            var line = "<div><img src='images/python.png' style = 'width:15pt; margin:2pt;'> <a style='cursor: pointer;' onclick='ShowOttoFileInput(\"" + filesArray[i] + "\")'>" + filesArray[i] + "</a></div>";
            filesArray[i] = line;
          }
        }

        for(var i = 1; i < filesArray.length; i++)
        {
          if(filesArray[i] != "directory.py" && filesArray[i] != "boot.py" && filesArray[i].indexOf(".py") > 0)
          {
            fileHTML += filesArray[i];
          }
        }

        $("#modalFilesText").html(fileHTML);
      }
    }

    if(message.indexOf('½') >= 0)
    {
        isFileInput = false;

        fileInput = fileInput.substring(fileInput.indexOf("?") + 1, fileInput.indexOf("½") - 1);

        if(connectionType == "Serial")
        {
      	   editorFileInput.setValue(fileInput);
    	  }
    	  else if(connectionType == "WebRepl")
    	  {
    	  	fileInput = fileInput + editorFileInput.getValue();
    	
    	  	fileInput = fileInput.replace(">>> print(f.read())", "");
    	  	fileInput = fileInput.replace(">>> print(", "");

    	  	editorFileInput.setValue(fileInput);
    	  }
    }

    if(message.indexOf('|') >= 0)
    {
      isFiles = false;
    }
    
    message = replaceAll(message, ">", "");
    message = replaceAll(message, "OK", "");
    message = replaceAll(message, "raw REPL; CTRL-B to exit", "");
    message = replaceAll(message, "aw REPL; CTRL-B to exit", "");
    message = replaceAll(message, "MPY: soft reboot", "");
    message = replaceAll(message, "Traceback (most recent call last):", "");
    message = replaceAll(message, "MPY: soft reboot ", "");
    message = replaceAll(message, "MicroPython v1.20.0 on 2023-04-26;", "");   
    message = replaceAll(message, "ESP module (1M) with ESP8266", ""); 
    message = replaceAll(message, "Type \"help()\" for more information.", "");                                                                                                                 
    message = replaceAll(message, "\n\r", "");
    
    return message;
}

async function disConnectSerial() {
  try
  {
    $("#modalConfirm").modal('hide');

    await writeSerial("04");
    reader.cancel();
    reader.releaseLock();
    await readableStreamClosed.catch(() => {  });

    writer.releaseLock();
    await port.close();

    DisconnectedSerialPort();
  }
  catch(err)
  {
    //console.log(err);
  }
}

async function writeSerial(send) {
  let data;
  if(send == "01")
    data = new Uint8Array([0x01]);
  else if(send == "02")
    data = new Uint8Array([0x02]); 
  else if(send == "03")
    data = new Uint8Array([0x03]);
  else if(send == "04")
    data = new Uint8Array([0x04]);

  await writer.write(data);
  await wait(10);
}

async function enter_row_repl()
{
    await writeSerial("03");
    await writeSerial("03");

    for (var i = 0; i < 5; i++ ) {
      await writeSerial("01");
    }

    await writeSerial("04");
    await writeSerial("03");
    await writeSerial("03");
}

async function exit_row_repl()
{
  await writeSerial("02");
}

async function deleteCommand(pythoncode)
{
  try
  {
    await enter_row_repl();
 
    await exec_raw_no_follow(pythoncode);
    
    await writeSerial("02");
  }
  catch(err)
  {
    console.log("Error: " + err.message)
  }
}

async function sendCommand(pythoncode)
{
  try
  {
    await enter_row_repl();
 
    await exec_raw_no_follow(pythoncode);
    
    await writeSerial("02");
    
    hideProgressPanel();
  }
  catch(err)
  {
    console.log("Error: " + err.message)
  }
}

async function SendString()
{
  try
  {
    //await writer.write(new TextEncoder().encode("AA"));
    //await writeSerial("64");

    var command = 
                "from ottobuzzer import OttoBuzzer \n" +
                "bz = OttoBuzzer(25) \n" +
                "bz.playNote(392, 1000) \n";
    sendCommand(command);
  }
  catch(err)
  {
    console.log("Error: " + err.message)
  }
}

async function saveCode(pythoncode, filename)
{
  await enter_row_repl();

  var command = "f = open('" + filename + "', 'wb')";
  await exec_raw_no_follow(command);

  //await writeSerial("04");
  pythoncode = pythoncode.replace(/(\r\n|\n|\r)/gm, '£');
  pythoncode = pythoncode.replace(/"/g, '\\"');
  
  //console.log(pythoncode);
  var elem = document.getElementById("progressBar"); 
  elem.innerHTML = '0%';
  elem.style.width = '0%'; 
  var width = 0;
  var parts = pythoncode.length / 310; // before it was 256
  var incrament = 100 / parts;

  for (var i = 0, s = pythoncode.length; i < s; i += 310) {
    var subcommand = pythoncode.slice(i, Math.min(i + 310, pythoncode.length));
    subcommand = subcommand.replace(/£/g, '\\n');
    console.log(subcommand);
    await exec_raw_no_follow('f.write("' + subcommand + '")');
    await wait(50);

    width += incrament; 
      
    if(Math.round(width) <= 100)
    {
      elem.innerHTML = Math.round(width) * 1  + '%';
      elem.style.width = Math.round(width) + '%'; 
    }
  }

  await exec_raw_no_follow("f.close()");

  await exit_row_repl();

  hideProgressPanel();
  showModalDialog(SaveCodeMessageText, "success");
  BeepSound();

  setTimeout(function() {
     writeSerial("04");
  }, 100);
}

async function saveLibrary(pythoncode, filename)
{
  await enter_row_repl();

  var command = "f = open('" + filename + "', 'wb')";
  await exec_raw_no_follow(command);

  //await writeSerial("04");
  pythoncode = pythoncode.replace(/(\r\n|\n|\r)/gm, '£');
  pythoncode = pythoncode.replace(/"/g, '\\"');
  
  for (var i = 0, s = pythoncode.length; i < s; i += 310) {
    var subcommand = pythoncode.slice(i, Math.min(i + 310, pythoncode.length));
    subcommand = subcommand.replace(/£/g, '\\n');

    await exec_raw_no_follow('f.write("' + subcommand + '")');
    await wait(20);
  }

  await exec_raw_no_follow("f.close()");

  await exit_row_repl();
}

async function exec_raw_no_follow(command) {
  var enc = new TextEncoder(); // always utf-8
  let command_bytes = enc.encode(command);
  // write command
  for (var i = 0, s = command_bytes.length; i < s; i += 32) { //before it was 128
   let dataToSend = command_bytes.slice(i, Math.min(i + 32, command_bytes.length))
     await writer.write(dataToSend);
     await wait(50);
  }

  await writeSerial("04");
}

async function sendWebRplSetup()
{
  try
  {
    var pythoncode = "import webrepl_setup"
    await enter_row_repl();
 
    await exec_raw_no_follow(pythoncode);
    
    hideProgressPanel();
  }
  catch(err)
  {
    console.log("Error: " + err.message)
  }
}

async function writeWebRplCommand(command) {
  var enc = new TextEncoder(); 
  let command_bytes = enc.encode(command);
  await writer.write(command_bytes);

  var data = new Uint8Array([0x0d, 0x0a]);
  await writer.write(data);
}

async function DeactivateWebRepl()
{
  var code = 
    "import uos, machine \n" +
    "import gc \n" +
    "#import webrepl \n" +
    "#webrepl.start() \n" +
    "gc.collect() \n";

  await saveLibrary(code, "boot.py");

  $('#webReplCondition').text(ActivateWebReplText);
  showModalDialog(RestartOtto, "info");
}

async function ActivateWebRepl()
{
  var code = 
    "import uos, machine \n" +
    "import gc \n" +
    "import webrepl \n" +
    "webrepl.start() \n" +
    "gc.collect() \n";

  await saveLibrary(code, "boot.py");

  $('#webReplCondition').text(DeactivateWebReplText);
  showModalDialog(RestartOtto, "info");
}

async function WebReplConditionChange()
{
    if(webreplActive)
    {
      DeactivateWebRepl();
    }
    else
    {
      ActivateWebRepl();
    }
}

function SerialData(value) 
{
    try 
    {
        if (value == null || value == undefined)
            return;

        // Check if the value contains version information
        if (value.includes("MicroPython") && !initialVersionCheckDone) {
            const versionMatch = value.match(/MicroPython v([\d.]+)/);
            if (versionMatch) {
                const version = versionMatch[1];
                localStorage.setItem("micropythonVersion", version);

                // Compare versions
                const currentVersion = version.split('.').map(Number);
                const targetVersion = '1.22.2'.split('.').map(Number);

                // Check if version is exactly 1.22.2
                const isTargetVersion = currentVersion[0] === targetVersion[0] && 
                                      currentVersion[1] === targetVersion[1] && 
                                      currentVersion[2] === targetVersion[2];

               if (!isFiles && !initialVersionCheckDone) {
    if (!isTargetVersion) {
        swal({
            title: "⚠️ MicroPython Update Required",
            content: {
                element: "div",
                attributes: {
                    innerHTML: `
                        Your version: v${version}<br><br>
                        Required version: v1.22.2<br><br>
                        Please update your firmware using the button below:
                    `
                }
            },
            icon: "warning",
            buttons: {
                later: {
                    text: "Later",
                    value: null,
                    visible: true,
                },
                update: {
                    text: "Update Now",
                    value: true,
                    className: "swal-button--update"
                }
            },
            className: "text-center"
        }).then((willUpdate) => {
            if (willUpdate) {
                const espButton = document.querySelector("esp-web-install-button");
                if (espButton) {
                    espButton.shadowRoot.querySelector("button")?.click();
                }
            }
            // Hide the button after interaction
            document.getElementById("esp-button-wrapper").style.display = "none";
        });

        // Show the button below the popup
        setTimeout(() => {
            const wrapper = document.getElementById("esp-button-wrapper");
            if (wrapper) {
                wrapper.style.display = "block";
            }
        }, 100);
    } else {
        swal({
            title: "Connected! 🔌",
            text: `MicroPython v${version} ✅\nYou are on the correct version.`,
            icon: "success",
            button: "OK",
            className: "text-center"
        });
    }
    initialVersionCheckDone = true;
}

                return;
            }
        }

        if (isCheckFilesCorrect) {
            const missingLibraries = compareArrays(files.split("\r\n"), ottoLibraryFiles);
            if (missingLibraries && !initialVersionCheckDone) {
                showModalDialog("There are missing library files:\n" + missingLibraries, "info");
            }
            isCheckFilesCorrect = false;
        }

      value = value.replace("OK", "");
      value = value.replace(">", "");
  
      if(value.indexOf("ULT") == 0)
      {
        value = value.substring(3, value.indexOf("#"));
        localStorage.setItem("ULT", value);
      }
      else if(value.indexOf("FAL") == 0)
      {
        value = value.substring(3, value.indexOf("#"));
        localStorage.setItem("FAL", value);
      }
      else if(value.indexOf("FAR") == 0)
      {
        value = value.substring(3, value.indexOf("#"));
        localStorage.setItem("FAR", value);
      }
      else if(value.indexOf("FDL") == 0)
      {
        value = value.substring(3, value.indexOf("#"));
        localStorage.setItem("FDL", value);
      }
      else if(value.indexOf("FDR") == 0)
      {
        value = value.substring(3, value.indexOf("#"));
        localStorage.setItem("FDR", value);
      }
      else if(value.indexOf("BA") == 0)
      {
        localStorage.setItem("Microbit", "BA");
      }
      else if(value.indexOf("BB") == 0)
      {
        localStorage.setItem("Microbit", "BB");
      }
      else if(value.indexOf("A") == 0)
      {
        localStorage.setItem("Microbit", value);
      }
      else
      {
        localStorage.setItem("Microbit", "");
      }
    }
    catch(err)
    {
        console.log("Error: " + err.message);
    }
}

function BeepSound()
{
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  const audio = new AudioContext();

  myPlayer = new SoundPlayer(audio);
  myPlayer.play(500, 0.8, "sine");
  myPlayer.stop(0.5);
}

async function checkMicropythonVersion() {
  try {
    await sendCommand('import sys\nprint("Version:", sys.version)');
  } catch(err) {
    console.log("Error checking MicroPython version:", err);
  }
}