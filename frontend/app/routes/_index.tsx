import type { MetaFunction } from "@remix-run/node";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export default function Index() {
  return (
    <div>
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Impedit doloremque a nobis maiores ullam minima repellendus delectus aliquid expedita, rem officia alias obcaecati omnis distinctio saepe in, ratione provident libero?
      Lorem ipsum dolor, sit amet consectetur adipisicing elit. Non sit illum dignissimos? Odit repudiandae eveniet fuga. Culpa, accusantium? Praesentium ex esse in beatae, amet reiciendis unde rerum corrupti quas alias?
      Quaerat eum eaque vitae dignissimos, ipsam ducimus quas temporibus est distinctio ut sit. Ipsum officia perferendis natus possimus rem? Provident vitae nobis expedita libero, quibusdam ut incidunt iste veritatis quidem.
      Dolor maiores quidem esse perferendis dolorem illum, odit nisi numquam nobis ipsum! Nisi esse velit, ea vel qui unde laboriosam perferendis iste eius quas quod accusamus, animi ipsum quo modi.
      Iusto rerum optio voluptates error odio, obcaecati molestias tempore facilis quae inventore quisquam id totam eos vel magni commodi deleniti libero incidunt saepe neque ullam illo. Explicabo reiciendis numquam corrupti.
    </div>
  );
}

