// program to convert decimal to binary
function decimalToBinary(x) {
        let bin = 0;
    let ram = {}, i = 1, step = 1;

while (x != 0) { ram[remainder] = x % 2; //Type1+2

            console.log(`Step ${step++}: ${x}/2`);
        x = parseInt(x / 2);
bin = bin + ram[remainder] * i;

        i = i * 10;
    }
        console.log(`Binary: ${bin}`);
}