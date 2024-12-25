document.getElementById('studentForm').onsubmit = async (event) => {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const course = document.getElementById('course').value;
    const interests = document.getElementById('interests').value.split(',');

    const response = await fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            student_id: 'P101',  // Temporary static ID
            name,
            course,
            interests
        })
    });

    const data = await response.json();
    alert("Roadmap Generated! Check the console for the result.");
    console.log(data.roadmap);
};
