DELIMITER $$
CREATE DEFINER=root@localhost PROCEDURE createUser(
    IN p_firstname VARCHAR(45),
    IN p_lastname VARCHAR(45),
    IN p_username VARCHAR(45),
    IN p_dob VARCHAR(45),
    IN p_country VARCHAR(45),
    IN p_email VARCHAR(45),
    IN p_password VARCHAR(300)

)
BEGIN
    if ( select exists (select 1 from users where userName = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into users
        (
            userName,
            FirstName,
            LastName,
            Country,
            DOB
        )
        values
        (
            p_username,
            p_firstname,
            p_lastname,
            p_country,
            p_dob
        );

        insert into login_credentials
            (

                Email,
                Password

            )

        values
        (

            p_email,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;
