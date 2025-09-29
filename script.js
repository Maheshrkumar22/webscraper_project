

// Handle search button click
document.getElementById('searchBtn').addEventListener('click', async () => {
    const url = document.getElementById('urlInput').value;
    const cardGrid = document.getElementById('cardGrid');
    const errorMsg = document.getElementById('errorMsg');
    const loadingSpinner = document.getElementById('loading-spinner');

    // Clear previous content
    errorMsg.classList.add('hidden');
    loadingSpinner.classList.add('hidden');
    cardGrid.innerHTML = '';

    // Basic URL validation (optional, not required per your request)
    if (!url) {
        errorMsg.textContent = 'Please enter a URL';
        errorMsg.classList.remove('hidden');
        return;
    }

    try {
        // Real API call (replace mockApiResponse)
        loadingSpinner.textContent = 'Loading...';
        loadingSpinner.classList.remove('hidden');
        const response = await fetch(`https://127.0.0.1:8000/api/${encodeURIComponent(url)}`);
        const data = await response.json();
        

// The `parsed_data` will now be a proper JavaScript array of objects
      

        //const data = mockApiResponse; // Uncomment for testing with mock

        // Render cards
        data.forEach(profile => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                ${profile['img url'] 
                    ? `<img src="${profile['img url']}" alt="${profile.Name}" onerror="this.outerHTML='<div class=\\'placeholder-img\\'>Image Not Available</div>'">`
                    : `<div class="placeholder-img">Image not available</div>`}
                <h2 class="text-xl font-semibold mt-2">${profile.Name}</h2>
                <p class="text-gray-600">${profile.Designation}</p>
            `;
            cardGrid.appendChild(card);
            loadingSpinner.classList.add('hidden');
        });
    } catch (error) {
        errorMsg.textContent = 'Data Not Found';
        errorMsg.classList.remove('hidden');
        cardGrid.innerHTML = '';
    }
    finally {
      // 2. Hide the loading spinner after the fetch completes (success or failure)
      loadingSpinner.classList.add('hidden');
      loadingSpinner.textContent = '';
      //errorMsg.textContent = 'Paste proper URL';
  }
});
