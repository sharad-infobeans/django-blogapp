const grpdeleteIcons = document.querySelectorAll('.delete-grp-post');
    
	// Add click event listener to each delete icon
	grpdeleteIcons.forEach((grpdeleteIcon) => {
		grpdeleteIcon.addEventListener('click', (event) => {
			event.preventDefault();
	
			// Get the blog post ID from the data-id attribute
			const postId = grpdeleteIcon.dataset.id;
            const csrf = grpdeleteIcon.dataset.csrf;
			// Show the confirmation dialog
			const confirmed = confirm('Are you sure you want to delete this group post?');
	
			// If confirmed, perform the deletion
			if (confirmed) {
				// Send an AJAX request to delete the grp posts
				fetch(`/posts/delete/${postId}/`, {
					method: 'POST',
					headers: {
						'X-CSRFToken': csrf,
					},
				})
				.then((response) => {
					// Reload the page or perform any other desired action
                    if(response.status==200){
                        location.reload();
                    }else{
                        alert("Something went wrong");
                    }
					
				})
				.catch((error) => {
                    alert("Error: " +error.message);
					console.error(error);
				});
			}
		});
	});