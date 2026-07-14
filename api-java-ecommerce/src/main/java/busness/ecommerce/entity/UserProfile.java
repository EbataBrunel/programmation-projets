package busness.ecommerce.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Getter @Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String firstName;
    private String lastName;
    private String phone;
    private String address;
    private String country;
    private String city;
    private String borough;
    private String photo;

    @OneToOne
    @JoinColumn(name = "user_id")
    private User user;
}
