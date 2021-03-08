// https://www.programiz.com/javascript/examples/decimal-binary
function decimalToBinary(x) {
        let bin = 0;
    let ram = {}, i = 1, step = 1;

while (x != 0) { ram[remainder] = x % 2; // Added type 1 and type 2 changes

            console.log(`Step ${step++}: ${x}/2, Remainder = ${ram[remainder]}, Quotient = ${parseInt(x/2)}`);
        x = parseInt(x / 2);
bin = bin + ram[remainder] * i;

        i = i * 10;
    }
        console.log(`Binary: ${bin}`);
}