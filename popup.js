document.addEventListener('DOMContentLoaded',()=>{
  const urlInput=document.getElementById('urlInput');
  const refreshBtn=document.getElementById('refreshBtn');
  const generateBtn=document.getElementById('generateBtn');
  const downloadBtn=document.getElementById('downloadBtn');
  const blurCanvas=document.getElementById('blurCanvas');
  const qrCanvas=document.getElementById('qrCanvas');
  let currentUrl='';

  function drawBlur(){
    const ctx=blurCanvas.getContext('2d');
    const w=blurCanvas.width,h=blurCanvas.height;
    ctx.fillStyle="rgba(255,255,255,0.03)";
    ctx.fillRect(0,0,w,h);
  }

  async function getURL(){
    return new Promise(res=>{
      chrome.tabs.query({active:true,currentWindow:true},tabs=>{
        res((tabs[0]&&tabs[0].url)||"");
      });
    });
  }

  function makeQR(text){
    if(!text || text.trim() === ''){
      alert('Please wait for URL to load or refresh the page');
      return;
    }
    try {
      console.log('Generating QR for URL:', text);
      
      // Determine appropriate type number based on data length
      // Capacity for 8-bit byte mode with error correction level M:
      // Type 1: 16, Type 2: 26, Type 3: 42, Type 4: 62, Type 5: 84, Type 6: 106, Type 7: 122
      let typeNumber = 1;
      const dataLength = text.length;
      if (dataLength <= 16) typeNumber = 1;
      else if (dataLength <= 26) typeNumber = 2;
      else if (dataLength <= 42) typeNumber = 3;
      else if (dataLength <= 62) typeNumber = 4;
      else if (dataLength <= 84) typeNumber = 5;
      else if (dataLength <= 106) typeNumber = 6;
      else if (dataLength <= 122) typeNumber = 7;
      else {
        // For very long URLs, limit to type 7 (maximum supported)
        typeNumber = 7;
        console.warn('URL length (' + dataLength + ') exceeds maximum capacity (122). Using type 7.');
      }
      
      // Ensure type number doesn't exceed 7 (maximum in our table)
      if (typeNumber > 7) {
        typeNumber = 7;
      }
      
      // Always create a new QRCode instance to avoid caching issues
      const qr = new QRCode(typeNumber, 1); // Error correction level M (1)
      qr.addData(text); // Add the URL text
      qr.make(); // Generate the QR code
      
      // Clear canvas first
      const ctx = qrCanvas.getContext('2d');
      ctx.clearRect(0, 0, qrCanvas.width, qrCanvas.height);
      
      // Render QR code to canvas
      qr.renderToCanvas(qrCanvas);
      
      qrCanvas.style.display="block";
      document.getElementById('blurContainer').style.display="none";
      downloadBtn.disabled=false;
      
      console.log('QR code generated successfully for:', text);
    } catch(error) {
      console.error('Error generating QR code:', error);
      alert('Error generating QR code: ' + error.message + '\nPlease try with a shorter URL.');
    }
  }

  (async()=>{
    drawBlur();
    currentUrl=await getURL();
    urlInput.value=currentUrl;
  })();

  refreshBtn.onclick=async()=>{
    currentUrl=await getURL();
    urlInput.value=currentUrl;
  };

  generateBtn.onclick=async()=>{
    // Always get fresh URL when generating
    const url = await getURL();
    currentUrl = url;
    urlInput.value = url;
    makeQR(url);
  };

  downloadBtn.onclick=()=>{
    if(qrCanvas.style.display === "none" || downloadBtn.disabled){
      alert('Please generate a QR code first');
      return;
    }
    const a = document.createElement('a');
    a.href = qrCanvas.toDataURL('image/png');
    a.download = 'qr-code.png';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };
});