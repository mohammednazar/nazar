function calculateDownpayment() {
    const propertyValue = parseFloat(document.getElementById('propertyValue').value);
    const downpaymentPercentage = parseFloat(document.getElementById('downpaymentPercentage').value);
    const result = document.getElementById('downpaymentResult');

    if (isNaN(propertyValue) || isNaN(downpaymentPercentage)) {
        result.textContent = "Please enter valid numbers!";
        return;
    }

    const downpayment = propertyValue * (downpaymentPercentage / 100);
    result.textContent = `Your downpayment: $${downpayment.toFixed(2)}`;
}

function calculateEMI() {
    const loanAmount = parseFloat(document.getElementById('loanAmount').value);
    const annualInterestRate = parseFloat(document.getElementById('interestRate').value) / 100 / 12;
    const loanTerm = parseInt(document.getElementById('loanTerm').value) * 12;
    const result = document.getElementById('emiResult');

    if (isNaN(loanAmount) || isNaN(annualInterestRate) || isNaN(loanTerm)) {
        result.textContent = "Please enter valid numbers!";
        return;
    }

    const emi = loanAmount * annualInterestRate * Math.pow(1 + annualInterestRate, loanTerm) / (Math.pow(1 + annualInterestRate, loanTerm) - 1);
    result.textContent = `Your monthly EMI: $${emi.toFixed(2)}`;
}
