window.onload = function() {
    document.getElementById('showForm').addEventListener('click', function() {
        let form = document.getElementById('commentForm');
        form.style.display = (form.style.display === 'none') ? 'block' : 'none';
    });

    const replyButtons = document.querySelectorAll('.reply-button');
    replyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const replyForm = button.parentElement.querySelector('.reply-form');
            if (replyForm) {
                replyForm.style.display = (replyForm.style.display === 'none') ? 'block' : 'none';
            }
        });
    });

    const showChildrenButtons = document.querySelectorAll('.show-children-button');
    showChildrenButtons.forEach(button => {
        button.addEventListener('click', () => {
            const childrenContainer = button.parentElement.querySelector('.children-container');
            console.log(childrenContainer)
            if (childrenContainer) {
                if (childrenContainer.style.display === 'none') {
                    childrenContainer.style.display = 'block';
                    button.textContent = 'Скрыть ветку';
                } else {
                    childrenContainer.style.display = 'none';
                    button.textContent = 'Показать ветку';
                }
            }
        });
    });

    // Sorting
    const sortButtons = document.querySelectorAll('.sort-button');
    sortButtons.forEach(button => {
        button.addEventListener('click', () => {
            const column = button.getAttribute('data-column');
            sortComments(column);
        });
    });

    function sortComments(column) {
        const commentsList = document.querySelector('.main-table');
        const sortOrder = commentsList.classList.contains('asc') ? -1 : 1;

        const comments = Array.from(commentsList.querySelectorAll('.parent-comment'));
        comments.sort((a, b) => {
            const aValue = a.querySelector(`.block-${column}`).textContent;
            const bValue = b.querySelector(`.block-${column}`).textContent;

            return (aValue > bValue ? 1 : -1) * sortOrder;
        });

        comments.forEach(comment => commentsList.appendChild(comment));

        if (sortOrder === 1) {
        commentsList.classList.remove('desc');
        commentsList.classList.add('asc');
        } else {
            commentsList.classList.remove('asc');
            commentsList.classList.add('desc');
        }
    }

    // Display mini images
    const imageLinks = document.querySelectorAll('.open-image-modal');
    imageLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const originalPath = this.getAttribute('data-original');

            const modalContent = `
                <img src="${originalPath}" alt="Image">
            `;

            const modalContainer = document.createElement('div');
            modalContainer.classList.add('modal-container');
            modalContainer.innerHTML = modalContent;

            document.body.appendChild(modalContainer);
        });
    });

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal-container')) {
            event.target.remove();
        }
    });

    //Text files handle
    const textLinks = document.querySelectorAll('.open-text-modal');

    textLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const originalPath = this.getAttribute('data-original');

            fetch(originalPath)
                .then(response => response.text())
                .then(text => {
                    const modalContainer = document.createElement('div');
                    modalContainer.classList.add('modal-container');
                    modalContainer.innerHTML = `
                        <div class="modal-content">
                            <pre>${text}</pre>
                            <button class="close-modal">Close</button>
                        </div>
                    `;

                    document.body.appendChild(modalContainer);

                    const closeModal = modalContainer.querySelector('.close-modal');
                    closeModal.addEventListener('click', function() {
                        modalContainer.remove();
                    });
                })
                .catch(error => console.error('Error:', error));
        });
    });

}
