package busness.ecommerce.dto;

import busness.ecommerce.entity.Contact;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;
import java.util.List;

@Getter
@Setter
@AllArgsConstructor
public class ContactGroupByDateDto {
    private LocalDate date;
    private List<Contact> contacts;
}
