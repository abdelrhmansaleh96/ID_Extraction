<?php

/**
 * Egyptian ID OCR Integration Class
 * 
 * This class provides methods to integrate with the Egyptian ID OCR service
 * using direct Python execution from PHP.
 * 
 * @author Abdelrahman Saleh
 * @version 1.0.0
 */
class EgyptianIDOCR
{
    private $pythonPath;
    private $servicePath;
    private $timeout;
    private $dbConnection;
    
    /**
     * Constructor
     * 
     * @param string $pythonPath Path to Python executable (default: 'python3')
     * @param string $servicePath Path to the OCR service directory
     * @param int $timeout Timeout in seconds for OCR processing (default: 60)
     * @param PDO $dbConnection Database connection for storing results
     */
    public function __construct($pythonPath = 'python3', $servicePath = null, $timeout = 60, $dbConnection = null)
    {
        $this->pythonPath = $pythonPath;
        $this->servicePath = $servicePath ?: __DIR__ . '/../';
        $this->timeout = $timeout;
        $this->dbConnection = $dbConnection;
    }
    
    /**
     * Extract ID data from image URL using the OCR service
     * 
     * @param string $imageUrl URL of the image to process
     * @param bool $saveToDatabase Whether to save results to database
     * @return array|false Extracted data or false on failure
     */
    public function extractFromUrl($imageUrl, $saveToDatabase = true)
    {
        try {
            // Validate URL
            if (!filter_var($imageUrl, FILTER_VALIDATE_URL)) {
                throw new Exception('Invalid image URL provided');
            }
            
            // Prepare the Python command
            $command = $this->buildCommand($imageUrl);
            
            // Execute the command
            $output = $this->executeCommand($command);
            
            // Parse the output
            $result = $this->parseOutput($output);
            
            // Save to database if requested and connection available
            if ($saveToDatabase && $this->dbConnection) {
                $this->saveToDatabase($imageUrl, $result);
            }
            
            return $result;
            
        } catch (Exception $e) {
            error_log("Egyptian ID OCR Error: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Extract ID data from local image file
     * 
     * @param string $imagePath Path to the local image file
     * @param bool $saveToDatabase Whether to save results to database
     * @return array|false Extracted data or false on failure
     */
    public function extractFromFile($imagePath, $saveToDatabase = true)
    {
        try {
            // Validate file exists
            if (!file_exists($imagePath)) {
                throw new Exception('Image file does not exist: ' . $imagePath);
            }
            
            // Convert local file to URL for processing
            $imageUrl = 'file://' . realpath($imagePath);
            
            return $this->extractFromUrl($imageUrl, $saveToDatabase);
            
        } catch (Exception $e) {
            error_log("Egyptian ID OCR Error: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Build the Python command to execute
     * 
     * @param string $imageUrl URL of the image
     * @return string Command to execute
     */
    private function buildCommand($imageUrl)
    {
        $scriptPath = $this->servicePath . 'extract_single.py';
        return 'cd ' . escapeshellarg($this->servicePath) . ' && ' .
               escapeshellcmd($this->pythonPath) . ' ' . 
               escapeshellarg('extract_single.py') . ' ' . 
               escapeshellarg($imageUrl);
    }
    
    /**
     * Execute the Python command
     * 
     * @param string $command Command to execute
     * @return string Command output
     * @throws Exception If command fails
     */
    private function executeCommand($command)
    {
        $output = [];
        $returnCode = 0;
        
        // Execute command with timeout
        exec($command . ' 2>&1', $output, $returnCode);
        
        if ($returnCode !== 0) {
            throw new Exception('Command execution failed: ' . implode("\n", $output));
        }
        
        return implode("\n", $output);
    }
    
    /**
     * Parse the Python script output
     * 
     * @param string $output Raw output from Python script
     * @return array Parsed data
     * @throws Exception If parsing fails
     */
    private function parseOutput($output)
    {
        // Extract JSON from output (look for lines that start with {)
        $lines = explode("\n", $output);
        $jsonLine = '';
        
        foreach ($lines as $line) {
            $line = trim($line);
            if (strpos($line, '{') === 0) {
                $jsonLine = $line;
                break;
            }
        }
        
        if (empty($jsonLine)) {
            throw new Exception('No JSON found in output: ' . $output);
        }
        
        // Try to decode JSON output
        $jsonData = json_decode($jsonLine, true);
        
        if (json_last_error() === JSON_ERROR_NONE) {
            return $jsonData;
        }
        
        throw new Exception('Failed to parse JSON: ' . $jsonLine);
    }
    
    /**
     * Save extracted data to database
     * 
     * @param string $imageUrl Original image URL
     * @param array $data Extracted data
     * @return bool Success status
     */
    private function saveToDatabase($imageUrl, $data)
    {
        try {
            $sql = "INSERT INTO extracted_id_data 
                    (image_url, first_name, second_name, full_name, national_id, 
                     address, birth_date, governorate, gender, created_at) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())";
            
            $stmt = $this->dbConnection->prepare($sql);
            
            return $stmt->execute([
                $imageUrl,
                $data['first_name'] ?? '',
                $data['second_name'] ?? '',
                $data['full_name'] ?? '',
                $data['national_id'] ?? '',
                $data['address'] ?? '',
                $data['birth_date'] ?? '',
                $data['governorate'] ?? '',
                $data['gender'] ?? ''
            ]);
            
        } catch (Exception $e) {
            error_log("Database save error: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Get extraction history from database
     * 
     * @param int $limit Number of records to retrieve
     * @return array|false Array of records or false on failure
     */
    public function getHistory($limit = 50)
    {
        try {
            $sql = "SELECT * FROM extracted_id_data 
                    ORDER BY created_at DESC 
                    LIMIT ?";
            
            $stmt = $this->dbConnection->prepare($sql);
            $stmt->execute([$limit]);
            
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
            
        } catch (Exception $e) {
            error_log("Database query error: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Search extractions by national ID
     * 
     * @param string $nationalId National ID to search for
     * @return array|false Array of matching records or false on failure
     */
    public function searchByNationalId($nationalId)
    {
        try {
            $sql = "SELECT * FROM extracted_id_data 
                    WHERE national_id = ? 
                    ORDER BY created_at DESC";
            
            $stmt = $this->dbConnection->prepare($sql);
            $stmt->execute([$nationalId]);
            
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
            
        } catch (Exception $e) {
            error_log("Database search error: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Test the OCR service connection
     * 
     * @return bool True if service is working, false otherwise
     */
    public function testConnection()
    {
        try {
            // Test with a simple command
            $command = escapeshellcmd($this->pythonPath) . ' --version';
            exec($command, $output, $returnCode);
            
            return $returnCode === 0;
            
        } catch (Exception $e) {
            return false;
        }
    }
}
