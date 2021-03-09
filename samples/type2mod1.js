// program to convert decimal to binary
function convertToBinary(x) {
    let binary = 0;
    let remainder, i = 1, step = 1;
    while (x != 0) {
        remainder = x % 2;
        console.log(`Step ${step++}: ${x}/2`);
        x = parseInt(x / 2);
        binary = binary + remainder * i;
        i = i * 10;
    }
    console.log(`Binary: ${binary}`);
}