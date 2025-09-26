var scroller = document.querySelector("#scroller");
var template = document.querySelector('#post_template');
var sentinel = document.querySelector("#sentinel");
var counter = 0;

function loadItems(){
    fetch(`/news/load?c=${counter}`).then((response) => {
        return response.json();
    }).then((data) => {
        if(!data.length) {
            sentinel.innerHTML = "No more posts";
            return;
        }

        for (var i = 0; i < data.length; i++){
            let templateClone = template.content.cloneNode(true);
            templateClone.querySelector("#title").innerHTML = `${data[i][0]} : ${data[i][1]}`;
            templateClone.querySelector("#content").innerHTML = data[i][2];
            scroller.appendChild(templateClone);
            counter += 1;
        }
    }).catch((error) => {
        console.error('Error loading items:', error);
    });
}

var intersectionObserver = new IntersectionObserver(entries => {
    if (entries[0].intersectionRatio <= 0){
        return;
    }
    loadItems();
});
intersectionObserver.observe(sentinel);

loadItems();