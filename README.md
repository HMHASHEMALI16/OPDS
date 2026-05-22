## 📚 HM 16 LIBRARY – OPDS Catalog

Add this OPDS link to your E-Book Reader app:

<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">

<input id="opdsLink" 
value="https://hmhashemali16.github.io/OPDS/catalog.xml" 
readonly
style="width:350px;padding:8px;border-radius:6px;border:1px solid #ccc;">

<button onclick="
navigator.clipboard.writeText(
document.getElementById('opdsLink').value
);
this.innerText='✓ Copied';
setTimeout(()=>this.innerText='📋 Copy',1500);
">
📋 Copy
</button>

</div>

**Supported Apps:**  
• Moon+ Reader  
• FBReader  
• Librera  
• KOReader  
• PocketBook  
• KyBook  
• Readest
