package busness.ecommerce.dto;

import jakarta.persistence.Column;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;


@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ContactResponseDto {
    private Long id;
    private String lastname;
    private String firstname;
    private String email;
    private String subject;
    private String message;
    private Integer status;
    private LocalDateTime createdAt;
}
