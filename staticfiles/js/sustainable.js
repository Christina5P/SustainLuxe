document.addEventListener('DOMContentLoaded', function() {
    var carousel = document.getElementById('introCarousel');
    var slideTitle = document.getElementById('slideTitle');
    var slideSubtitle = document.getElementById('slideSubtitle');
    var slideContent = document.getElementById('slideContent');

    if (carousel && slideTitle && slideSubtitle && slideContent) {
      carousel.addEventListener('slide.bs.carousel', function (e) {
        switch(e.to) {
          case 0:
            slideTitle.textContent = "SHE Second Hand Effect";
            slideSubtitle.textContent = "Definition of Carbon Savings";
            slideContent.innerHTML = `
              <p>By "carbon savings," we refer to the amount of greenhouse gases, measured in carbon dioxide equivalents (CO₂e) in kilograms,
              required to produce a similar new item. By choosing second-hand products, you can make a positive impact by reducing the emissions
              associated with manufacturing new items.
                <h3>Assumptions Used in Our Carbon Savings Calculation</h3>
              <p>
                To estimate carbon savings, we have made a few assumptions based on various sources. We collect data on the materials used in the clothing we handle.
                Based on this, we make assumptions about the material composition of each garment to calculate an average carbon savings figure per item.
              </p>
              <h3>Sources Used</h3>
              <ul>
                <li>The HIGG MSI, Materials Sustainability Index</li>
                <li>Charitable Reuse</li>
                <li>Textile Exchange</li>
              </ul>
              </p>
            `;
            break;
          case 1:
            slideTitle.textContent = "Make Sustainable Choices";
            slideSubtitle.textContent = "Benefits of Second-Hand Shopping";
            slideContent.innerHTML = `
              <p>In an era where environmental concerns are at the forefront of global discussions, our fashion choices have never been more impactful. The fashion industry is known for its significant environmental footprint, from textile waste to pollution and resource consumption. Fortunately, there's a stylish and eco-conscious solution at hand – second-hand shopping. In this blog post, we'll explore the many environmental benefits of embracing second-hand fashion and how it contributes to a more sustainable future.
        </p>

        <ul>
          <li><strong>1. Reducing Textile Waste:</strong> The fashion industry is notorious for its disposable culture, with millions of tons of clothing ending up in landfills each year. Second-hand shopping helps combat this problem by giving clothing a second life. When you purchase pre-owned items, you're diverting them from the waste stream, reducing the demand for new production, and extending their usability.</li>

          <li><strong>2. Lower Carbon Footprint:</strong> The production of new clothing involves numerous processes, from growing or manufacturing fibers to transportation and distribution. All of these contribute to greenhouse gas emissions. Second-hand shopping requires significantly fewer resources and reduces the carbon footprint associated with fashion, making it a more eco-friendly choice.</li>

          <li><strong>3. Conserving Resources:</strong> Creating new garments consumes vast amounts of water, energy, and raw materials. Second-hand shopping conserves these valuable resources by extending the lifespan of clothing. By choosing second-hand, you help reduce the strain on our planet's limited resources.</li>

          <li><strong>4. Promoting Ethical Consumption:</strong> When you buy second-hand, you're not supporting the often unethical labor practices that can be associated with fast fashion. Instead, you're promoting a more ethical form of consumption by valuing and appreciating items that already exist.</li>

          <li><strong>5. Encouraging Circular Fashion:</strong> Second-hand shopping is a prime example of a circular fashion economy, where clothing is used and reused, rather than discarded after a short period. This model helps close the loop on fashion production and encourages a more sustainable industry.</li>

          <li><strong>6. Discovering Unique Pieces:</strong> Vintage and second-hand stores offer a wide range of unique and one-of-a-kind items. By choosing pre-loved pieces, you're not only reducing waste but also expressing your individual style in a way that's distinct from mass-produced fashion.</li>
        </ul>
            `;
            break;
          case 2:
            slideTitle.textContent = "Discover Unique Style";
            slideSubtitle.textContent = "Express Yourself Sustainably";
                slideContent.innerHTML = `
            <p>As consumers, we have a responsibility to make conscious choices that benefit the environment. Here are some ways we can contribute:</p>
            <ul>
              <li>Choose second-hand items whenever possible</li>
              <li>Donate or sell clothes you no longer wear</li>
              <li>Repair and upcycle clothing instead of discarding</li>
              <li>Support brands with sustainable practices</li>
              <li>Educate others about the benefits of second-hand shopping</li>
            </ul>
            `;
            break;
        }
      });
    } else {
      console.error('One or more required elements are missing from the DOM');
    }
});
  
    // Scroll to top
     $(document).ready(function () {
        $('.btt-link').click(function(e) {
            e.preventDefault();  
            window.scrollTo(0, 0);
        });
       }); 
