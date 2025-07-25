document.getElementById("searchForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    // Get form data
    const query = document.getElementById("query").value;
    const model = document.getElementById("model").value;
    const top_n = document.getElementById("top_n").value;
    const timeDiv = document.getElementById("time");

    // Make the API request
    const response = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, model, top_n: parseInt(top_n) })
    });
    // Handle the response
    const data = await response.json();
    const resultsDiv = document.getElementById("results");
    if (response.ok) {
        resultsDiv.innerHTML = `
            <h1>Результаты поиска:</h1>
            <ul>
                ${data.results.map(result => `<li>${result}</li>`).join("")}
            </ul>
        `;
        timeDiv.innerHTML = `<p><strong>Время поиска:</strong> ${data.time_taken} секунд</p>`;
    } else {
        resultsDiv.innerHTML = `<p style="color: red;">Ошибка: ${data.detail}</p>`;
        timeDiv.innerHTML = '';
    }
});
