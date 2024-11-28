-- Create a new table called "example_table"
CREATE TABLE IF NOT EXISTS example_table (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  value INT NOT NULL
);

-- Insert some sample data into the "example_table"
INSERT INTO example_table (name, value) VALUES ('Sample 1', 100);
INSERT INTO example_table (name, value) VALUES ('Sample 2', 200);
INSERT INTO example_table (name, value) VALUES ('Sample 3', 300);