// --- STATE ---
let currentColumns = [];
let numericColumns = [];

// --- NAVIGATION ---
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-links li').forEach(el => el.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    // Find li with onclick containing the tabId
    const navItems = document.querySelectorAll('.nav-links li');
    navItems.forEach(item => {
        if(item.getAttribute('onclick').includes(tabId)) {
            item.classList.add('active');
        }
    });
}

// --- API HELPERS ---
async function postData(url, formData) {
    const response = await fetch(url, {
        method: 'POST',
        body: formData
    });
    return response.json();
}

function updateSelects(columns, selectIds, isNumeric=false) {
    selectIds.forEach(id => {
        const select = document.getElementById(id);
        const selected = Array.from(select.selectedOptions).map(opt => opt.value); // Keep selection if possible
        select.innerHTML = '';
        
        columns.forEach(col => {
            const option = document.createElement('option');
            option.value = col;
            option.text = col;
            if(selected.includes(col)) option.selected = true;
            select.appendChild(option);
        });
    });
}

function renderTable(data, containerId) {
    if(!data || data.length === 0) {
        document.getElementById(containerId).innerHTML = '<p>No hay datos.</p>';
        return;
    }
    
    const cols = Object.keys(data[0]);
    let html = '<table><thead><tr>';
    cols.forEach(c => html += `<th>${c}</th>`);
    html += '</tr></thead><tbody>';
    
    data.forEach(row => {
        html += '<tr>';
        cols.forEach(c => html += `<td>${row[c]}</td>`);
        html += '</tr>';
    });
    html += '</tbody></table>';
    
    document.getElementById(containerId).innerHTML = html;
}

// --- HANDLERS ---

// 1. Upload
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.innerText = "Cargando...";
    
    try {
        const res = await postData('/api/upload', formData);
        
        if (res.error) {
            statusDiv.innerText = "Error: " + res.error;
            return;
        }
        
        statusDiv.innerText = `Carga Exitosa. Shape: (${res.shape[0]}, ${res.shape[1]})`;
        renderTable(res.preview, 'uploadPreview');
        
        // Update State
        currentColumns = res.columns;
        numericColumns = res.numeric_columns;
        
        // Detect 'Cluster' if re-uploading processed file
        if(currentColumns.includes('Cluster') && !numericColumns.includes('Cluster')) {
             // Force Cluster to stay if we want, but typically upload resets state
        }

        // Update Dropdowns
        updateSelects(currentColumns, ['nullCols']);
        updateSelects(numericColumns, ['scaleCols', 'clusterCols', 'plotCol', 'plotX', 'plotY']);
        
    } catch (err) {
        console.error(err);
        statusDiv.innerText = "Error de conexión.";
    }
});

// 2. Clean Nulls
async function cleanNulls() {
    const cols = Array.from(document.getElementById('nullCols').selectedOptions).map(o => o.value);
    const method = document.getElementById('nullMethod').value;
    
    if(cols.length === 0) { alert("Seleccione columnas."); return; }
    
    const formData = new FormData();
    cols.forEach(c => formData.append('cols', c));
    formData.append('method', method);
    
    const res = await postData('/api/clean/nulls', formData);
    document.getElementById('cleanStatus').innerText = res.message;
    if(res.preview) renderTable(res.preview, 'uploadPreview'); // Update preview
}

// 3. Scale
async function scaleData() {
    const cols = Array.from(document.getElementById('scaleCols').selectedOptions).map(o => o.value);
    const method = document.getElementById('scaleMethod').value;
    
    if(cols.length === 0) { alert("Seleccione columnas."); return; }
    
    const formData = new FormData();
    cols.forEach(c => formData.append('cols', c));
    formData.append('method', method);
    
    const res = await postData('/api/clean/scale', formData);
    document.getElementById('cleanStatus').innerText = res.message;
    if(res.preview) renderTable(res.preview, 'uploadPreview');
}

// 4. Stats
async function loadStats() {
    const res = await fetch('/api/stats').then(r => r.json());
    if(res.error) { alert(res.error); return; }
    
    // Simple markdown render for now, or just pre
    // Ideally we would parse the MD table to HTML, but text is fine
    let html = `<pre>${res.descriptive}</pre>`;
    
    if(res.correlation) {
         // Could render heatmap here or json table
         const corr = JSON.parse(res.correlation);
         // ... render corr table logic if needed ...
    }
    document.getElementById('statsOutput').innerHTML = html;
}

// 5. Cluster
async function runCluster() {
    const cols = Array.from(document.getElementById('clusterCols').selectedOptions).map(o => o.value);
    const k = document.getElementById('kSlider').value;
    
    if(cols.length < 2) { alert("Seleccione al menos 2 variables."); return; }
    
    const formData = new FormData();
    cols.forEach(c => formData.append('cols', c));
    formData.append('k', k);
    
    const res = await postData('/api/cluster', formData);
    document.getElementById('clusterStatus').innerText = res.message;
    if(res.preview) {
        renderTable(res.preview, 'uploadPreview');
        currentColumns = Object.keys(res.preview[0]); 
        // Add Cluster to options? Usually it's numeric/categorical mixed.
        // Assuming Cluster is numeric (int), it might need to be added to numeric lists
        if(!numericColumns.includes('Cluster')) numericColumns.push('Cluster');
        updateSelects(numericColumns, ['plotCol', 'plotX', 'plotY', 'clusterCols']);
    }
}

// 6. Plot
function updatePlotInputs() {
    const type = document.getElementById('plotType').value;
    const col = document.getElementById('plotCol');
    const x = document.getElementById('plotX');
    const y = document.getElementById('plotY');
    
    col.style.display = 'none';
    x.style.display = 'none';
    y.style.display = 'none';
    
    if(type === 'distribution') {
        col.style.display = 'block';
    } else if (type === 'regression' || type === 'cluster') {
        x.style.display = 'block';
        y.style.display = 'block';
    }
    // correlation needs no inputs
}

async function generatePlot() {
    const type = document.getElementById('plotType').value;
    const formData = new FormData();
    formData.append('type', type);
    
    if(type === 'distribution') {
        formData.append('col', document.getElementById('plotCol').value);
    } else if (type === 'regression' || type === 'cluster') {
         formData.append('x', document.getElementById('plotX').value);
         formData.append('y', document.getElementById('plotY').value);
    }
    
    const res = await postData('/api/plot', formData);
    if(res.error) { alert(res.error); return; }
    
    Plotly.newPlot('mainPlot', res.data, res.layout);
}

// Init
updatePlotInputs();
