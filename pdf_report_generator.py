from fpdf import FPDF
import csv
from datetime import datetime

def read_data(filename):
    """Read data from a CSV file and return as a list of dictionaries."""
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []

def analyze_data(data):
    """Analyze data and return statistics (avg, min, max for numeric columns)."""
    if not data:
        return {}
    
    numeric_columns = []
    for col in data[0].keys():
        try:
            float(data[0][col])  # Check if column is numeric
            numeric_columns.append(col)
        except (ValueError, TypeError):
            pass  # Skip non-numeric columns
    
    stats = {
        'record_count': len(data),
        'columns': list(data[0].keys()),
        'numeric_columns': numeric_columns,
    }
    
    for col in numeric_columns:
        values = [float(row[col]) for row in data]
        stats[f'{col}_avg'] = sum(values) / len(values)
        stats[f'{col}_min'] = min(values)
        stats[f'{col}_max'] = max(values)
    
    return stats

def generate_pdf_report(data, stats, output_filename):
    """Generate a PDF report with analysis results."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # 1. Title Section
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Data Analysis Report", ln=1, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1, align='C')
    pdf.ln(10)  # Add space

    # 2. Summary Statistics
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Summary Statistics", ln=1)
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 8, txt=f"Total records analyzed: {stats['record_count']}", ln=1)
    pdf.cell(200, 8, txt=f"Columns in dataset: {', '.join(stats['columns'])}", ln=1)
    pdf.ln(5)

    # 3. Numeric Columns Analysis (if any)
    if stats['numeric_columns']:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Numeric Columns Analysis", ln=1)
        pdf.set_font("Arial", size=12)
        
        for col in stats['numeric_columns']:
            pdf.cell(200, 8, txt=f"Column: {col}", ln=1)
            pdf.cell(200, 8, txt=f"  - Average: {stats[f'{col}_avg']:.2f}", ln=1)
            pdf.cell(200, 8, txt=f"  - Minimum: {stats[f'{col}_min']:.2f}", ln=1)
            pdf.cell(200, 8, txt=f"  - Maximum: {stats[f'{col}_max']:.2f}", ln=1)
            pdf.ln(3)  # Small space after each column

    # 4. Sample Data Table (First 10 rows)
    pdf.add_page()  # New page for the table
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Sample Data (First 10 Rows)", ln=1)
    pdf.set_font("Arial", size=10)

    if data:
        col_widths = [30, 40, 20, 30, 40]  # Custom column widths
        headers = data[0].keys()

        # Table Header
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, txt=header, border=1, align='C')
        pdf.ln()

        # Table Rows (First 10)
        for row in data[:10]:
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, txt=str(row[header]), border=1)
            pdf.ln()

    # Save the PDF
    pdf.output(output_filename)
    print(f"✅ Report saved as: {output_filename}")

def main():
    input_filename = "sample_data.csv"  # Change this to your file
    output_filename = "analysis_report.pdf"

    data = read_data(input_filename)
    if not data:
        return  # Exit if no data
    
    stats = analyze_data(data)
    generate_pdf_report(data, stats, output_filename)

if __name__ == "__main__":
    main()
