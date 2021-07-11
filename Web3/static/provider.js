function display_choice() {
    const choice = document.querySelector("input[name='choice']:checked")
    location.replace(`http://127.0.0.1:8000/pages/${choice.value}`)
    console.log(choice.value)
}

