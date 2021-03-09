// program to convert decimal to binary
function convertToBinary(x) {
    let bin = 0;
    let rem, i = 1, step = 1;
    while (x != 0) {
        rem = x % 2;
        console.log(`Step ${step++}: ${x}/2`);
        x = parseInt(x / 2);
        bin += rem * i;
        i *= 10;
    }
    console.log(`Binary: ${bin}`);
}