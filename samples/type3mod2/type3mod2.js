// program to convert decimal to binary
function convertToBinary(x) {
    let rem, i = 1, step = 1;
    let bin = 0;
    while (x != 0) {
        rem = x % 2;
        console.log(`Step ${step++}: ${x}/2`);
        bin = bin + rem * i;
        i = i * 10;
        x = parseInt(x / 2);
    }
    console.log(`Binary: ${bin}`);
}