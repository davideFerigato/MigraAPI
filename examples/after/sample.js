// Example JavaScript code with new API
const newApi = require('new-api');
const { getUserById, getUserPosts } = require('new-api');

function main() {
    const client = newApi.createClient({ key: 'secret' });
    
    // Direct call
    const user = newApi.getUserById(123);
    console.log(user);
    
    // Destructured call
    const posts = getUserPosts(123);
    
    // Client instance call
    const data = client.getUserPosts(123);
    
    return { user, posts, data };
}

main();
