// https://www.programiz.com/javascript/examples/decimal-binary
function convertToBinary(x) {
    let bin = 0;
    let rem, i = 1, step = 1;
	let bool = (x != 0)
    while (bool) {
        rem = x % 2;
        console.log(`Step ${step++}: ${x}/2, Remainder = ${rem}, Quotient = ${parseInt(x/2)}`);
        x = parseInt(x / 2);
        bin = bin + rem * i;
        i = i * 10;
		bool = (x != 0)
    }
    console.log(`Binary: ${bin}`);
}