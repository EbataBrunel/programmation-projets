package busness.ecommerce.dto;


import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ContactRequestDto {
    private String lastname;
    private String firstname;
    private String email;
    private String subject;
    private String message;
}
