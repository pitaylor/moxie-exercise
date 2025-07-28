INSERT INTO medspas (name, address, phone_number, email_address) VALUES 
('Glow MedSpa', '123 Wellness Blvd, Beverly Hills, CA 90210', '(310) 555-0123', 'info@glowmedspa.com')
ON CONFLICT (name) DO NOTHING;
INSERT INTO medspas (name, address, phone_number, email_address) VALUES 
('Radiant Wellness', '456 Serenity Way, Newport Beach, CA 92660', '(949) 555-0456', 'hello@radiantwellness.com')
ON CONFLICT (name) DO NOTHING;
