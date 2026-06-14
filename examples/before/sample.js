// Example JavaScript code with deprecated API
const oldApi = require('old-api');
const { getUser, fetchPosts } = require('old-api');

function main() {
    const client = oldApi.createClient({ key: 'secret' });
    
    // Direct call
    const user = oldApi.getUser(123);
    console.log(user);
    
    // Destructured call
    const posts = fetchPosts(123);
    
    // Client instance call
    const data = client.fetchPosts(123);
    
    return { user, posts, data };
}

main();
